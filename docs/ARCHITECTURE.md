# Martabak Core: Architecture Walkthrough

How the whole system fits together, from the browser to the encrypted bytes in storage.
Written from the Person 1 (crypto) point of view.

## 1. Big picture

```
 ┌──────────────┐        HTTPS         ┌──────────────────────────────────────┐
 │   Browser    │ ───────────────────► │  Vercel (serverless, read-only FS)   │
 │ Jinja2 pages │ ◄─────────────────── │  api/index.py ──► main.py (FastAPI)  │
 │ + Tailwind   │   HTML / JSON / file │                                      │
 └──────────────┘                      │  ┌─────────┐ ┌──────────┐ ┌────────┐ │
   cookie: session_token               │  │ routers/│ │  core/   │ │ models │ │
                                       │  │ auth    │ │ cipher   │ │ User   │ │
                                       │  │ vault   │ │ key_mgr  │ │ Vault  │ │
                                       │  └────┬────┘ │ inspector│ │ File   │ │
                                       │       │      │ storage  │ └───┬────┘ │
                                       │       │      │ auth_sec │     │      │
                                       │       │      └────┬─────┘     │      │
                                       └───────┼───────────┼───────────┼──────┘
                                               │           │           │
                      ┌────────────────────────┼───────────┘           │ SQLAlchemy
                      │ Supabase Storage REST  │                       ▼
                      ▼ (httpx, service key)   │              ┌──────────────────┐
        ┌─────────────────────────┐            │              │ Supabase Postgres│
        │ bucket: encrypted-storage│◄───────────┘              │  users           │
        │   <uuid>.enc  (cipher-   │                           │  vault_files     │
        │   text only)             │                           │  (METADATA ONLY: │
        ├─────────────────────────┤                           │  key_id, iv_hex, │
        │ bucket: keys             │                           │  cipher, owner)  │
        │   <uuid>.key (raw keys)  │                           └──────────────────┘
        └─────────────────────────┘
   No Supabase env vars? ──► LocalStorageClient: ./encrypted_storage and ./keys
```

## 2. Folder map

```
martabak-core/
├── main.py            FastAPI app, HTML page routes (/, /login, /signup, /vault/{id}/inspect)
├── config.py          loads .env; refuses to boot without SECRET_KEY / DATABASE_URL
├── database.py        SQLAlchemy engine + get_db + init_db        (P2)
├── api/index.py       Vercel entrypoint, imports app              (P2)
├── models/            User, VaultFile tables                      (P2)
├── schemas/           pydantic in/out shapes                      (P2)
├── routers/
│   ├── auth_router.py register, login, signup, logout, /me       (P2)
│   └── vault_router.py upload, list, download, inspect, delete   (P2, calls core/)
├── core/                                                          (P1)
│   ├── cipher_engine.py  AES-CBC / DES-CBC / RC4 encrypt+decrypt
│   ├── key_manager.py    save/load/delete/exists key by UUID
│   ├── storage_client.py Supabase vs local, picks backend at runtime
│   ├── inspector.py      entropy, hex dump, block map, avalanche
│   └── auth_security.py  bcrypt + HMAC token + get_current_user
├── templates/ static/    UI                                       (P3)
├── benchmarks/runner.py  writes report_data.json                  (P4)
└── tests/                cipher + key manager tests, backend API tests
```

## 3. The cipher engine

| Cipher | Key | Mode | IV | Padding |
|---|---|---|---|---|
| AES | 32 bytes (AES-256) | CBC | random 16 bytes | PKCS7 |
| DES | 8 bytes | CBC | random 8 bytes | PKCS7 |
| RC4 | 16 bytes | stream | none | none |

- A fresh random key (`os.urandom`) and IV are generated on every encrypt call.
- ECB is never used anywhere. Tests assert that `ECB` is rejected.
- `encrypt_data(bytes, cipher)` returns `{ciphertext, key, iv, mode, cipher_type}`.
- `decrypt_data(ciphertext, key, cipher, iv)` returns the original bytes.

## 4. Upload flow (encrypt)

```
Browser ── POST /api/v1/vault/upload (file, file_type, cipher_choice, cookie) ──►
   │
   ▼
get_current_user ── decode HMAC token ── check exp ── load User from DB ── else 401
   │
   ▼
validate: cipher in {AES,DES,RC4}, file_type in {personal_data,id_scan,office_doc,video},
          file not empty
   │
   ▼
MartabakCipherEngine.encrypt_data(bytes, cipher)
   │        ┌── AES: key=32B, IV=16B random, pad(PKCS7), CBC
   │        ├── DES: key= 8B, IV= 8B random, pad(PKCS7), CBC
   │        └── RC4: key=16B, no IV, stream XOR
   ▼
 { ciphertext, key, iv, mode }
   │
   ├──► KeyManager.save_key(key, key_id=uuid4)    ──► bucket "keys"/<key_id>.key
   ├──► storage.upload(ciphertext, uuid4.enc)     ──► bucket "encrypted-storage"
   └──► INSERT vault_files(user_id, file_type, original_filename,
                           encrypted_filepath, cipher_used, cipher_mode,
                           key_id, iv_hex, file_size)
   │
   ▼
Response: JSON, or 303 redirect to /?uploaded=1 if browser form
```

## 5. Download flow (decrypt)

```
GET /api/v1/vault/download/{id}
   │
   ▼
get_current_user (401 if bad)
   │
   ▼
SELECT * FROM vault_files WHERE id=:id AND user_id=:me      <- tenant isolation
   │   none? ──► 404 "not found or access denied"
   ▼
storage.download("encrypted-storage", encrypted_filepath)   ──► ciphertext
KeyManager.load_key(key_id)                                  ──► key   (bucket "keys")
iv = bytes.fromhex(iv_hex) or None
   │
   ▼
MartabakCipherEngine.decrypt_data(ciphertext, key, cipher, iv)
   │      block ciphers: CBC decrypt then unpad;  RC4: XOR keystream
   ▼
Response(bytes, Content-Disposition: attachment; filename=<basename>)
```

## 6. Inspector flow

```
GET /vault/{id}/inspect   (HTML)    or    GET /api/v1/vault/{id}/inspect (JSON)
   │
   ▼  same owner check, load ciphertext + key
inspect_vault_payload()
   ├─ calculate_entropy(ciphertext)       Shannon H, 0..8 bits/byte
   ├─ generate_hex_dump(first 256 B)      16 B/row, offset + hex + ascii
   ├─ generate_block_map(cipher, len)     AES 16B, DES 8B, RC4 1B units
   └─ compute_avalanche_demo(cipher,key)  random block P1, flip 1 bit -> P2
                                          same key+IV, encrypt both, count
                                          differing bits
                                          AES/DES ~ 50%,  RC4 = exactly 1 bit
   ▼
inspect.html renders it
```

## 7. Authentication

```
signup/login ──► bcrypt hash/verify (first 72 bytes of password)
              ──► token = base64(payload{sub,exp}) . base64(HMAC-SHA256(SECRET_KEY, payload))
              ──► Set-Cookie session_token (httponly, samesite=lax)

every request: split token -> recompute HMAC -> compare_digest -> check exp -> load User
(also accepts "Authorization: Bearer <token>" for API use)
```

## 8. What each store knows

```
 Postgres vault_files        keys bucket           encrypted-storage bucket
 ┌─────────────────────┐    ┌────────────────┐    ┌────────────────────────┐
 │ who owns it         │    │ raw key bytes  │    │ ciphertext bytes       │
 │ original filename   │    │ by key_id      │    │ by random uuid.enc     │
 │ cipher, mode, IV    │    └────────────────┘    └────────────────────────┘
 │ key_id (pointer)    │
 │ enc filename (ptr)  │    Decrypting needs all three:
 └─────────────────────┘    DB row (pointers + IV) + key + ciphertext
```

A database dump alone yields pointers and IVs, with no keys and no data.
Whoever holds the Supabase service-role key can read both buckets, so the
separation between keys and ciphertext is logical, not physical.

## 9. Storage backend switch

`core/storage_client.get_storage()` decides at runtime:

```
SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY set ──► SupabaseStorageClient (REST over httpx)
otherwise                                    ──► LocalStorageClient (./encrypted_storage, ./keys)
```

`KeyManager` uses the same switch. Passing an explicit `keys_dir` forces the
local backend, which is how the unit tests stay offline. Object names are
reduced to a basename everywhere, so a tampered DB value cannot traverse
directories.

## 10. Tests and benchmarks

```
tests/test_cipher_engine.py ──► engine + KeyManager (local tmp dirs, no network)
tests/test_backend_api.py   ──► FastAPI TestClient: auth, isolation, full upload -> download
benchmarks/runner.py        ──► engine only: 1KB/500KB/5MB x AES/DES/RC4 x 5 runs,
                                tracemalloc peak, median ms, MiB/s -> report_data.json
```

## 11. Known weak spots (be ready to discuss)

- **No tamper protection.** CBC and RC4 here have no MAC or AEAD, so modified
  ciphertext is not detected, only sometimes surfaces as a padding error.
- **Error detail leaks.** The download route returns `Decryption failed: {e}` to
  the client, which can act as a padding oracle for CBC.
- **Key separation is logical.** Same Supabase project and service-role key for both buckets.
- **DES and RC4 are broken ciphers.** They are required by the assignment, and the report should say so.
- **Silent cleanup failures.** `delete_vault_file` swallows storage and key deletion errors.
- **Whole file in memory.** Fine for the 5 MB benchmark, risky for large videos.
- **Minor:** the session cookie has no `secure=True`; `config.py` creates local dirs at import time.
