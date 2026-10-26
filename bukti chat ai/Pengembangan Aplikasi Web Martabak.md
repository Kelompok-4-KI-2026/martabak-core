# Chat Conversation

Note: _This is purely the output of the chat conversation and does not contain any raw data, codebase snippets, etc. used to generate the output._

### User Input

Saya ada project tentang Merancang dan bangun sebuah aplikasi web untuk skenario Databse sebuah karyawan pada usaha martabak. untuk lebih lengkap nya anda boleh baca ini: /home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core/README.md. dan anda bisa lihat isi repo ini : /home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core. saya juga menyarankan anda untuk melihat prd nya yang berada di dalam branch git switch feature/add-team-prds . analisa dulu saja jika sudah beri tahu saya

### Planner Response

Baik, izinkan saya membaca README dan melihat struktur repo terlebih dahulu, sekaligus mengecek PRD di branch `feature/add-team-prds`.

*Listed directory [martabak-core](file:///home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core) *

*Listed directory [core](file:///home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core/core) *

*Listed directory [routers](file:///home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core/routers) *

*Listed directory [models](file:///home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core/models) *

*Listed directory [docs](file:///home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core/docs) *

### Planner Response

Sekarang saya lihat isi file-file kode yang sudah ada:

*Listed directory [templates](file:///home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core/templates) *

*Listed directory [schemas](file:///home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core/schemas) *

*Listed directory [benchmarks](file:///home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core/benchmarks) *

### Planner Response

Analisis selesai. Berikut ringkasan lengkapnya:

---

## 🍫 Analisis: Martabak Core

### 📋 Gambaran Umum

Ini adalah proyek **Tugas 1 Mata Kuliah Keamanan Informasi** — sebuah web app franchise martabak yang berfungsi sebagai **secure vault** untuk menyimpan dokumen sensitif secara terenkripsi. Proyek dikerjakan oleh **tim 4 orang** dan dibuat dari scratch.

---

### 🗂️ Status Repo Saat Ini

> **Hampir semua file masih KOSONG.** Struktur direktori sudah disiapkan, tapi isinya belum ada.

| File / Modul | Status |
|---|---|
| `main.py` | ❌ Kosong |
| `database.py` | ❌ Kosong |
| `config.py` | ❌ Kosong |
| `core/cipher_engine.py` | ❌ Kosong |
| `core/key_manager.py` | ❌ Kosong |
| `routers/auth_router.py` | ❌ Kosong |
| `routers/vault_router.py` | ❌ Kosong |
| `routers/benchmark_router.py` | ❌ Kosong |
| `models/user.py` | ❌ Belum dicek |
| `templates/base.html` | ❌ Kosong |
| `benchmarks/runner.py` | ❌ Kosong |

---

### 🏗️ Arsitektur yang Dirancang

```
Browser → FastAPI → Crypto Engine (AES/DES/RC4)
                  ↓                     ↓
           PostgreSQL DB        /encrypted_storage/*.enc
         (metadata & users)
```

**Tech stack:**
- **Backend:** FastAPI + Uvicorn
- **Database:** PostgreSQL + SQLAlchemy ORM
- **Frontend:** Jinja2 Templates + Tailwind CSS via CDN
- **Crypto:** `pycryptodome` (AES-CBC, DES-CBC, RC4)
- **Auth:** `passlib[bcrypt]` + session-based

---

### 👥 Pembagian Tugas (4 PRD)

| Person | Role | Branch | Tanggung Jawab |
|---|---|---|---|
| **P1** | Crypto Specialist | `feature/crypto-engine` | `core/cipher_engine.py`, `core/key_manager.py` — AES/DES/RC4, no-ECB |
| **P2** | Backend Dev | `feature/backend-api` | `database.py`, `models/`, `routers/auth_router.py`, `routers/vault_router.py`, `main.py` |
| **P3** | Frontend Dev | `feature/frontend-ui` | `templates/base.html`, `dashboard.html`, `login.html` — Tailwind dark mode |
| **P4** | Benchmark & Writer | `feature/benchmark-and-docs` | `benchmarks/runner.py`, `report_data.json`, Laporan 2 halaman A4 |

---

### ⚠️ Constraint Penting

1. **No ECB Mode** — wajib pakai CBC atau Stream cipher
2. **User Isolation** — user hanya bisa akses file miliknya sendiri (`user_id` check)
3. **4 tipe data:** `personal_data`, `id_scan`, `office_doc`, `video`
4. **3 cipher:** AES-256-CBC, DES-CBC, RC4
5. **Laporan 2 halaman A4** dengan benchmark nyata + analisis
6. **Branch discipline** — tidak boleh push langsung ke `main`

---

### 🚀 Apa yang Perlu Dibangun

Secara sederhana, **semua kode belum ditulis**. Proyek baru punya:
- ✅ Struktur folder & file placeholder
- ✅ Semua 4 PRD (blueprint detail)
- ✅ `requirements.txt` dengan dependensi lengkap
- ✅ `AGENT_INSTRUCTIONS.md` sebagai panduan tim

---

### ❓ Pertanyaan untuk Anda

Mau saya bantu mulai dari mana? Saya bisa:
1. **Mulai dari scratch** — build semua layer satu per satu
2. **Fokus pada role tertentu** — misalnya kamu Person 1 (Crypto), saya bantu crypto engine-nya saja
3. **Build everything** — saya kerjakan seluruh proyek sesuai PRD untuk semua person

### User Input

jangan gunakan emote. jawab singkat

### Planner Response

Analisis selesai.

Ringkasan:
1. Proyek: Sistem database/vault terenkripsi karyawan & waralaba Martabak Core (Tugas 1 Keamanan Informasi).
2. Kebutuhan: Enkripsi 4 kategori data (personal_data, id_scan, office_doc, video) menggunakan 3 cipher (AES-CBC, DES-CBC, RC4). Mode ECB dilarang. Isolasi akses per pengguna wajib.
3. Status repo: Struktur folder dan 4 dokumen PRD sudah lengkap, tetapi file kode masih kosong.
4. Pembagian PRD:
   - PRD 1: Crypto engine (AES, DES, RC4).
   - PRD 2: Backend FastAPI, database PostgreSQL/SQLAlchemy, upload/download vault.
   - PRD 3: Frontend Jinja2 + Tailwind UI.
   - PRD 4: Benchmark runner dan draf laporan 2 halaman A4.

Langkah berikutnya: Tentukan bagian mana yang ingin dikerjakan terlebih dahulu.

### User Input

baik saya bertugas sebagai backend, saya mempunyai banyak skill yang bisa anda gunakan di ~/.config/opencode/skills/. saya minta anda susun plan dulu untuk apa yang harus saya lakukan? dan anda bisa cek yang crypto specialist sudah selesai pekerjaanya atau belum. plan dulu apa saja yang harus kita lakukan

### Planner Response

Baik, saya cek skills dan status crypto specialist sekaligus.

*Listed directory [skills](file:///home/rasyaarya/.config/opencode/skills) *

### Planner Response

Skills tidak dapat diakses (permission denied). Cek juga git log untuk melihat apakah ada commit dari crypto specialist:

- [ ] `config.py` — env vars, secret key, setting dasar
- [ ] `database.py` — koneksi PostgreSQL via SQLAlchemy
- [ ] `models/user.py` — model tabel `users`
- [ ] `models/vault_file.py` — model tabel `vault_files`

**Fase 2 — Auth**

- [ ] `schemas/auth_schema.py` — Pydantic schema untuk register/login
- [ ] `routers/auth_router.py` — endpoint register, login (session/token based)
- [ ] Integrasi `passlib[bcrypt]` untuk hashing password

**Fase 3 — Vault Core**

- [ ] `schemas/vault_schema.py` — Pydantic schema response vault
- [ ] `routers/vault_router.py` — POST `/upload` (encrypt + simpan ke disk + DB), GET `/files` (list file milik user), GET `/download/{file_id}` (decrypt + serve)
- [ ] User isolation: setiap endpoint vault verifikasi `user_id` dari session/token

**Fase 4 — App Entry Point**

- [ ] `main.py` — inisialisasi FastAPI, mount routers, create tables, serve Jinja2 templates

**Fase 5 — Integrasi Crypto**

- [ ] Hubungkan `MartabakCipherEngine` ke vault router
- [ ] Test round-trip: upload → enkripsi → simpan → download → dekripsi → file identik

---

### Pertanyaan Sebelum Mulai

Ada beberapa hal yang perlu Anda tentukan:

1. **Autentikasi:** Pakai JWT token atau session cookie (HTTP session)?
2. **Crypto blocker:** Saya buatkan stub dulu agar bisa jalan paralel, atau tunggu Person 1?
3. **Skills:** Path `/home/rasyaarya/.config/opencode/skills/` tidak bisa dibaca (permission denied). Bisa Anda cek isi foldernya dan beritahu skill apa yang relevan?

### User Input

coba anda periksa di branch lain, crypto specialist sudah dikerjakan, dan frontend juga sudah

### Planner Response

Kedua branch sudah selesai. Berikut statusnya:

---

### Status Pemeriksaan

**Crypto (Person 1) — SELESAI**
- `cipher_engine.py`: Implementasi lengkap — AES-256-CBC, DES-CBC, RC4, no ECB, dengan `verify_integrity()`
- `key_manager.py`: Lengkap — simpan/load/hapus key ke file binary `keys/<uuid>.key` dengan permission `0o600`
- 35 test round-trip passed

**Frontend (Person 3) — SELESAI**
- `base.html`, `dashboard.html`, `login.html`: Sudah ada — dark mode, Tailwind CDN, drag-drop upload, cipher badges, vault search/filter, loading state button

---

### Kontrak yang Harus Dipatuhi Backend

Dari crypto specialist, backend perlu:

| Aksi | Fungsi |
|---|---|
| Enkripsi | `MartabakCipherEngine.encrypt_data(file_bytes, cipher_type)` → returns `{ciphertext, key, iv, mode, cipher_type}` |
| Simpan key | `KeyManager.save_key(key, key_id)` → key file di `keys/<uuid>.key` |
| Dekripsi | `MartabakCipherEngine.decrypt_data(ciphertext, key, cipher_type, iv)` |
| Load key | `KeyManager.load_key(key_id)` |

Dari frontend, endpoint yang dibutuhkan:

| Route | Method | Kegunaan |
|---|---|---|
| `/login` | POST | Login dengan email + password |
| `/` atau `/dashboard` | GET | Render dashboard |
| `/api/v1/vault/upload` | POST | Upload + enkripsi file (multipart: `file`, `file_type`, `cipher_choice`) |
| `/api/v1/vault/files` | GET | List file milik user (untuk render tabel vault) |
| `/api/v1/vault/download/{file_id}` | GET | Dekripsi + download file |

---

### Plan Backend — Final

**Fase 1 — Foundation**
- [ ] `config.py` — env vars & settings
- [ ] `database.py` — PostgreSQL + SQLAlchemy
- [ ] `models/user.py` + `models/vault_file.py` — ORM models (tambah kolom `key_id`, `iv_hex`)

**Fase 2 — Auth**
- [ ] `schemas/auth_schema.py` — Pydantic schemas
- [ ] `routers/auth_router.py` — POST `/register`, POST `/login`, GET `/logout`, session cookie

**Fase 3 — Vault**
- [ ] `schemas/vault_schema.py` — response schemas
- [ ] `routers/vault_router.py` — upload, list, download + integrasi `KeyManager`

**Fase 4 — Entry Point**
- [ ] `main.py` — init app, mount routers, create tables, serve templates

Siap mulai? Saya rekomendasikan mulai dari **Fase 1 (Foundation)** dulu. Mau langsung kita kerjakan?

### User Input

ya  mari kit aeksekusi dan nanti akan saya audit

   - Inisialisasi engine & session SQLAlchemy (dukungan PostgreSQL & SQLite fallback).
   - Model `User`: username, email, hashed_password, created_at.
   - Model `VaultFile`: user_id, file_type, original_filename, encrypted_filepath, cipher_used, cipher_mode, key_id, iv_hex, file_size.

2. **Authentication & Security (`core/auth_security.py`, `routers/auth_router.py`, `schemas/auth_schema.py`)**
   - Password hashing menggunakan bcrypt standar (trunckasi aman 72-byte).
   - Signed session token berbasis HMAC-SHA256 untuk API Bearer token dan browser session cookie (`session_token`).
   - Endpoint register, login (API & Form submit), logout, dan `/api/v1/auth/me`.

3. **Vault Lifecycle (`routers/vault_router.py`, `schemas/vault_schema.py`)**
   - `POST /api/v1/vault/upload`: Validasi kategori data (`personal_data`, `id_scan`, `office_doc`, `video`) dan cipher (`AES`, `DES`, `RC4`). Enkripsi file, simpan key via `KeyManager`, simpan ciphertext ke `encrypted_storage/*.enc`, dan catat metadata ke DB.
   - `GET /api/v1/vault/files`: Mengambil daftar file milik pengguna aktif saja.
   - `GET /api/v1/vault/download/{file_id}`: Strict user isolation (cek kepemilikan), load key via `KeyManager`, dekripsi sesuai cipher dan IV, kirim binary file utuh.
   - `DELETE /api/v1/vault/files/{file_id}`: Hapus ciphertext, hapus file key, dan hapus record DB.

4. **Entry Point & UI Integration (`main.py`)**
   - Integrasi router FastAPI dan Jinja2 template rendering (`dashboard.html` dan `login.html`).
   - Pembuatan skema DB otomatis pada startup.

5. **Pengujian (`tests/test_backend_api.py`)**
   - Health check.
   - Register & login workflow.
   - Enkripsi, upload, dan verifikasi integritas binary download (AES, DES, RC4).
   - Strict User Isolation (User B ditolak saat mengakses file User A).
   - Status: 41 test passed (35 crypto + 6 backend).

Semua commit dibuat secara atomic dan siap diaudit.

### User Input

baik sebelum kita lanjut saya inign anda jelaskan semuanya. termasuk workflow dll

### Planner Response

Berikut penjelasan arsitektur, keamanan, dan alur kerja (workflow) sistem Martabak Core.

---

### 1. Skenario dan Kebutuhan

Sistem ini adalah portal data waralaba (franchise) martabak yang dirancang untuk kepatuhan UU PDP dan GDPR. Sistem mengelola 4 jenis aset:
- **Personal Data**: Teks/data PII mitra waralaba.
- **Identity Document Scans**: Gambar pindaian KTP / NPWP.
- **Office Documents**: Dokumen formula/resep rahasia adonan (PDF/DOCX).
- **Videos**: Video SOP dapur resolusi tinggi (MP4).

---

### 2. Arsitektur Komponen

```
[ Klien / Browser ]
        |
        v (HTTP Form / JSON Bearer)
[ FastAPI Server ]
   ├── Auth Middleware (Bcrypt + HMAC Session Token)
   ├── Input Validation (Format data, tipe cipher)
   └── Crypto Engine (core/cipher_engine.py)
        |
        +---> [ core/key_manager.py ] -----> [ keys/<uuid>.key ] (Izin file 0600)
        +---> [ Disk Storage ] -------------> [ encrypted_storage/<uuid>.enc ]
        +---> [ Database (PostgreSQL/SQLite) ] (Tabel users, vault_files)
```

1. **Frontend**: Jinja2 + Tailwind CSS (halaman login dan dashboard terisolasi).
2. **Backend**: FastAPI dengan router modular (`auth_router` dan `vault_router`).
3. **Database**: SQLAlchemy ORM untuk menyimpan metadata file dan data autentikasi (kunci enkripsi **tidak pernah** disimpan di database).
4. **Crypto Engine**: Implementasi AES-256-CBC, DES-CBC, dan RC4 stream cipher via `pycryptodome`.
5. **Key Storage**: Kunci simetris disimpan terpisah di direktori `keys/` dengan restriksi permission UNIX `0600` (hanya owner yang bisa membaca).

---

### 3. Workflow Lengkap

#### A. Alur Autentikasi (Register & Login)
1. User mendaftar melalui form/API (`POST /api/v1/auth/register`).
2. Password di-hash menggunakan algoritma **Bcrypt** (dibatasi 72-byte untuk mencegah wrap-bug) dan disimpan di tabel `users`.
3. Saat login (`POST /login` atau `POST /api/v1/auth/login`), kredensial diverifikasi.
4. Sistem membuat signed token berbasis **HMAC-SHA256** (berisi `user_id` dan `expiration`).
5. Token dikirim sebagai:
   - Cookie `session_token` bertipe `HttpOnly; SameSite=Lax` untuk akses browser.
   - Properti `access_token` JSON untuk klien API / Swagger UI.

#### B. Alur Enkripsi & Unggah File (`POST /api/v1/vault/upload`)
1. User mengirim multipart request: file biner, kategori (`personal_data`, `id_scan`, `office_doc`, `video`), dan pilihan cipher (`AES`, `DES`, `RC4`).
2. Server memvalidasi autentikasi user melalui `get_current_user`.
3. Byte mentah file dibaca ke memori.
4. `MartabakCipherEngine.encrypt_data` dipanggil:
   - Dibuat kunci acak (`os.urandom`) sesuai spesifikasi cipher (AES: 32 bytes, DES: 8 bytes, RC4: 16 bytes).
   - Untuk cipher blok (AES, DES), dibuat IV acak dan data di-padding dengan PKCS7 mode CBC. Mode ECB dilarang.
   - Untuk cipher aliran (RC4), data langsung dienkripsi tanpa IV.
5. Server membuat `key_id` bertipe UUID. Kunci biner disimpan ke file `keys/<key_id>.key` via `KeyManager`.
6. Ciphertext biner disimpan ke `encrypted_storage/<uuid>.enc`.
7. Metadata disimpan ke database: nama asli file, kategori, algoritma yang digunakan, mode cipher, `key_id`, dan representasi hex dari IV.

#### C. Alur Pengunduhan & Dekripsi (`GET /api/v1/vault/download/{file_id}`)
1. Server mengecek identitas pemohon dari session token.
2. **Strict User Isolation**: Query database memastikan `VaultFile.id == file_id` DAN `VaultFile.user_id == current_user.id`. Jika file milik user lain, sistem langsung mengembalikan `HTTP 404 (Access Denied)`.
3. Ciphertext dibaca dari `encrypted_storage/<uuid>.enc`.
4. Kunci privat diambil dari filesystem via `KeyManager.load_key(file_record.key_id)`.
5. `MartabakCipherEngine.decrypt_data` mendekripsi data:
   - AES/DES: Dekripsi CBC dengan IV tersimpan, dilanjutkan unpad PKCS7.
   - RC4: Inversi keystream XOR.
6. Server mengembalikan biner asli yang identik 100% dengan header `Content-Disposition: attachment; filename="<original_filename>"`.

#### D. Alur Penghapusan (`DELETE /api/v1/vault/files/{file_id}`)
1. Verifikasi kepemilikan file oleh user yang login.
2. File biner terenkripsi (`.enc`) dihapus dari disk.
3. File kunci (`.key`) dihapus secara permanen via `KeyManager.delete_key`.
4. Baris metadata pada tabel `vault_files` dihapus dari database.

---

### 4. Skema Database

```sql
-- Tabel users
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel vault_files
CREATE TABLE vault_files (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    file_type VARCHAR(50) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    encrypted_filepath VARCHAR(500) NOT NULL,
    cipher_used VARCHAR(20) NOT NULL,
    cipher_mode VARCHAR(20) NOT NULL,
    key_id VARCHAR(100) NOT NULL,
    iv_hex VARCHAR(64),
    file_size INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 5. Cara Menjalankan & Memverifikasi

1. **Menjalankan Server**:
   ```bash
   .venv/bin/uvicorn main:app --reload --port 8000
   ```
   - Dashboard: `http://localhost:8000`
   - Dokumentasi Swagger API: `http://localhost:8000/docs`

2. **Menjalankan Pengujian Otomatis**:
   ```bash
   PYTHONPATH="." .venv/bin/pytest -p no:launch_testing -v
   ```
   Seluruh 41 pengujian (35 crypto unit test + 6 backend integration & user isolation test) saat ini lulus 100%.

*Grep searched codebase*

### Planner Response

### Penyebab Error

Error terjadi pada `templates/base.html` baris 92:
```jinja2
{% with messages = get_flashed_messages(with_categories=true) %}
```
`get_flashed_messages` adalah fungsi bawaan Flask, sedangkan aplikasi ini dibangun di atas FastAPI/Starlette Jinja2Templates yang tidak menyediakan fungsi tersebut secara default, sehingga Jinja2 melempar:
`jinja2.exceptions.UndefinedError: 'get_flashed_messages' is undefined` saat merender halaman `/login`.

---

### Solusi yang Diterapkan

1. **Registrasi Global Jinja2**:
   Mendaftarkan fungsi `get_flashed_messages` ke dalam environment Jinja2 di `main.py`:
   ```python
   def get_flashed_messages(with_categories: bool = False):
     return []

   templates.env.globals["get_flashed_messages"] = get_flashed_messages
```
2. **Alias Route Dashboard**:
   Menambahkan routing `@app.get("/dashboard")` sejajar dengan `@app.get("/")` agar link navigasi dashboard di `base.html` bekerja.
3. **Standarisasi Parameter `TemplateResponse`**:
   Menyesuaikan urutan parameter `TemplateResponse(request=request, name=..., context=...)` sesuai konvensi Starlette terkini.
4. **Pengujian Tambahan**:
   Menambahkan unit test perenderan halaman HTML `/login` dan proteksi redirect `/dashboard` ke `tests/test_backend_api.py`.

Semua 43 test otomatis kini lulus (100% passed). Anda sudah dapat menjalankan ulang:
```bash
.venv/bin/uvicorn main:app --reload --port 8000
```

### User Input

baik jadi apa lagi yang belum kita lakukan?? jika ini sudah final menurut anda gunakan skill web-audit untuk mengaudit semuanya

*Listed directory [martabak-core](file:///home/rasyaarya/kampus/sem3/keamanan_informasi/martabak-core) *

   - File `benchmarks/runner.py` masih kosong.
   - File `benchmarks/report_data.json` belum digenerate.
   - Draf laporan 2 halaman A4 (analisis komparasi performa AES vs DES vs RC4 pada payload PII 1KB, Dokumen 500KB, dan Video 5MB) belum disusun.

2. **Penggabungan Branch Tim (Git Merge ke `main`)**
   - Branch `feature/crypto-engine`, `feature/frontend-ui`, dan `feature/backend-api` masih terpisah dan belum dimerge secara resmi ke `main`.

---

### Hasil Audit Aplikasi Web (Web & Security Audit)

Audit dilakukan pada seluruh lapisan aplikasi yang telah dibangun:

#### 1. Kontrol Akses & Isolasi Pengguna (Broken Access Control - OWASP A01)
- **Status: LULUS**
- **Temuan**: Endpoint pengunduhan (`/api/v1/vault/download/{id}`) dan penghapusan (`/api/v1/vault/files/{id}`) memvalidasi secara ketat kepemilikan data (`VaultFile.user_id == current_user.id`). Permintaan dari pengguna lain langsung menghasilkan `404 Not Found (Access Denied)`. Pengujian regresi otomatis membuktikan isolasi 100% efektif.

#### 2. Kriptografi & Manajemen Kunci (Cryptographic Failures - OWASP A02)
- **Status: LULUS**
- **Temuan**:
  - Larangan ECB dipatuhi: AES dan DES menggunakan mode CBC dengan inisialisasi IV acak (`os.urandom`) setiap pemanggilan.
  - Kunci enkripsi tidak disimpan di dalam database PostgreSQL/SQLite. Kunci disimpan terpisah di direktori `keys/<uuid>.key` dengan hak akses file dibatasi ke `0600` (read/write hanya owner).
  - Integritas data terverifikasi identik (exact binary match) setelah siklus enkripsi-dekripsi untuk seluruh format (teks, dokumen, biner).

#### 3. Autentikasi & Session (Identification and Authentication Failures - OWASP A07)
- **Status: LULUS**
- **Temuan**:
  - Password di-hash menggunakan algoritma Bcrypt standar dengan per-password salt.
  - Session token ditandatangani menggunakan HMAC-SHA256, menyertakan masa kedaluwarsa (`exp`), dan diverifikasi menggunakan pembandingan waktu konstan (`hmac.compare_digest`) guna mencegah serangan timing attack.
  - Cookie session dikonfigurasi dengan flag `HttpOnly=True` dan `SameSite=Lax`.

#### 4. Validasi Input & Penyimpanan File Terenkripsi (Security Misconfiguration & Injection - OWASP A03/A05)
- **Status: LULUS**
- **Temuan**:
  - Whitelist ketat diterapkan pada pilihan cipher (`AES`, `DES`, `RC4`) dan tipe file (`personal_data`, `id_scan`, `office_doc`, `video`).
  - File terenkripsi disimpan dengan nama berbasis UUID acak (`<uuid>.enc`), bukan nama asli file. Hal ini mencegah serangan Path Traversal maupun overwriting file sistem.
  - Header unduhan menggunakan `Path(original_filename).name` untuk mensterilkan karakter traversal saat file disajikan kembali ke pengguna.

#### 5. Rekomendasi Tambahan (Optional Hardening)
- **Anti-CSRF**: Meskipun cookie `SameSite=Lax` memblokir sebagian besar serangan Cross-Site Request Forgery antar domain, penambahan token anti-CSRF eksplisit pada form HTML merupakan praktik penguatan tambahan jika ingin standar enterprise.
- **Rate Limiting**: Menambahkan pembatasan percobaan login pada endpoint `POST /login` untuk mitigasi serangan brute-force.

Semua 43 test otomatis saat ini berstatus hijau (100% passed). Langkah berikutnya yang tersisa adalah menyelesaikan tugas **Person 4 (Benchmark Runner dan Laporan A4)**.

### User Input

baik untuk uji web nya apa yang harus saya lakukan? dan juga saya belum merge branch ini kan?

Branch Anda saat ini adalah `feature/backend-api`. Branch `main` belum berisi perubahan backend, crypto, maupun frontend yang ada di branch ini. Jangan merge ke `main` sebelum Anda selesai menguji.

---

### 2. Panduan Menguji Aplikasi Web di Browser

Server Uvicorn saat ini sudah aktif di terminal Anda pada port 8000 (`http://localhost:8000`).

Ikuti langkah pengujian berikut:

#### Langkah A: Buat Akun Pengguna Uji
Buka tab terminal baru atau gunakan `curl` untuk membuat akun pertama:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "franchisee_aceh", "email": "aceh@martabak.id", "password": "Password123!"}'
```
*(Atau buka `http://localhost:8000/docs` lalu uji endpoint `POST /api/v1/auth/register`)*

#### Langkah B: Uji Login Web
1. Buka browser ke alamat `http://localhost:8000/login`.
2. Masukkan email: `aceh@martabak.id` dan password: `Password123!`.
3. Klik tombol **Sign In to Vault**. Anda akan diarahkan ke halaman Dashboard (`http://localhost:8000/dashboard`).

#### Langkah C: Uji Enkripsi & Unggah File
Pada form di sebelah kiri Dashboard:
1. Pilih **Data Category** (misal: *Office Document* atau *Identity Document*).
2. Pilih **Cipher**:
   - Coba **AES-256** (Default).
   - Ulangi dengan **DES** dan **RC4**.
3. Pilih sembarang file (PDF, gambar KTP, atau teks).
4. Klik **Encrypt & Store Securely**.
5. File akan muncul pada tabel **Encrypted Vault Registry** di sebelah kanan lengkap dengan badge cipher yang dipilih.

#### Langkah D: Uji Dekripsi & Pengunduhan
1. Klik tombol **Decrypt & Download** pada baris file di tabel.
2. Buka file hasil unduhan dan pastikan file terbuka normal serta isinya identik 100% dengan file asli sebelum diunggah.

#### Langkah E: Uji Filter & Logout
1. Ketik nama file di kolom pencarian *"Filter files..."* di atas tabel untuk memastikan pencarian realtime berfungsi.
2. Klik **Sign Out** di kanan atas navbar untuk memastikan sesi berakhir dan redirect kembali ke halaman `/login`.

---

### 3. Cara Merge Setelah Selesai Uji

Jika pengujian manual Anda berhasil dan siap diaudit tim:
```bash
git checkout main
git merge feature/backend-api
```

### Planner Response

Berikut penjelasan lengkap tentang **di mana data disimpan dan bagaimana Anda melihat ciphertext-nya**.

---

### Penyimpanan Data: 3 Lokasi Terpisah (by design)

#### 1. Database (`martabak.db`) — Metadata Saja

Database **tidak menyimpan isi file sama sekali**, hanya metadata:

| Kolom | Isi | Contoh |
|---|---|---|
| `id` | ID record | 13 |
| `user_id` | Pemilik file | 7 |
| `original_filename` | Nama asli | `Teks paragraf Anda.png` |
| `cipher_used` | Algoritma | `DES` |
| `cipher_mode` | Mode cipher | `CBC` |
| `key_id` | UUID penunjuk kunci | `6c8d0a8d-...` |
| `iv_hex` | Initialization Vector (hex) | `0bfbf10a3cf4a853` |
| `file_size` | Ukuran file asli (bytes) | 1.209.138 |

#### 2. `keys/<uuid>.key` — Kunci Enkripsi Biner

File kunci menyimpan **kunci simetris biner mentah**. Ukurannya:
- AES → 32 bytes (256-bit)
- DES → 8 bytes (64-bit)
- RC4 → 16 bytes (128-bit)

Contoh isi file `6c8d0a8d-...key` (kunci DES):
```
00000000: 0352 4bce 70e6 23d4    .RK.p.#.
```
Hanya 8 byte biner acak — ini adalah kunci DES-CBC untuk file ID 13.

Permission: **`-rw-------` (0600)** — hanya owner yang bisa membaca.

#### 3. `encrypted_storage/<uuid>.enc` — Ciphertext Biner

File `.enc` berisi **ciphertext murni** hasil enkripsi. Tidak ada header, tidak ada metadata — hanya stream biner acak.

Contoh pembacaan hex 20 baris pertama dari file 1.2MB (dari ciphertext file gambar PNG terenkripsi DES):
```
00000000: d9ab 8b36 7173 7ed3 8623 915e 4637 ffd0  ...6qs~..#.^F7..
00000010: d728 309a 23d6 f103 e45d 837c 60e9 e84f  .(0.#....].|`..O
```
Tidak ada satupun informasi yang bisa dibaca — ini adalah tujuan dari enkripsi.

---

### Visualisasi Hubungan 3 Komponen

```
Database (vault_files)
  ├── key_id: "6c8d0a8d..."  ──────────────────────► keys/6c8d0a8d...key   (KUNCI 8 byte DES)
  ├── iv_hex: "0bfbf10a..."  (disimpan di DB)
  └── encrypted_filepath: "encrypted_storage/da5e596e...enc" ──► da5e596e...enc (CIPHERTEXT 1.2MB)

Saat download:
  DB cari record → ambil key_id → load key dari file → ambil iv_hex dari DB → decrypt → file asli
```

**Kenapa dipisah?** Jika database bocor (SQL Injection), penyerang hanya mendapat metadata — tidak ada kunci dan tidak ada ciphertext. Jika disk bocor, penyerang hanya punya ciphertext tanpa kunci.

### User Input

baiklah sekarang saya minta merge yang backend dan crypto speciailst dulu, lalu jika sudah cek ulang apakah ada conflict

### Planner Response

Working tree bersih — tidak ada perubahan yang perlu di-commit. Merge commit yang dibuat tadi (`22c2ac2`) sudah menjadi commit terakhir di `main`.

Anda hanya perlu **push** ke remote:

```bash
git push origin main
```

Jika ingin verifikasi log commit terakhir sebelum push:
```bash
git log --oneline -5
```

### User Input

ini kan kalau digunakan oleh orang lain tidak bisa karena database nya bersifat lokal? bagaimana caranya agar bisa orang lain menambahkannya lewat laptop dia dan tetap masuk ke database saya? apa gunakan supabase?

### Planner Response

Betul sekali. SQLite bersifat **lokal** — file `martabak.db` ada di laptop Anda, tidak bisa diakses orang lain dari luar. Ada beberapa solusi, saya jelaskan pilihan yang paling cocok untuk konteks tugas kuliah ini:

---

### Opsi yang Tersedia

#### 1. Supabase (PostgreSQL Cloud — Recommended untuk tugas ini)
**Gratis, mudah, dan sudah PostgreSQL** — cocok karena `requirements.txt` sudah ada `psycopg2-binary`.

Yang perlu dilakukan:
1. Daftar di [supabase.com](https://supabase.com) → buat project baru.
2. Supabase otomatis memberikan **connection string** PostgreSQL berformat:
   ```
   postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
   ```
3. Ganti `DATABASE_URL` di `config.py`:
   ```python
   DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:...")
   ```
4. Jalankan server Anda. Tabel otomatis dibuat via `Base.metadata.create_all()`.
5. Semua orang yang mengakses server Anda (atau jika di-deploy) akan terhubung ke database yang sama.

**Catatan penting:** Supabase **hanya mengganti database**. Server FastAPI tetap berjalan di laptop Anda. Jika Anda ingin orang lain mengakses dari laptop mereka, Anda juga perlu **expose server**-nya (lihat opsi 3).

---

#### 2. Neon.tech (PostgreSQL Cloud Serverless — Alternatif)
Mirip Supabase, gratis, format connection string sama persis. Tidak perlu konfigurasi tambahan.

---

#### 3. Expose Server ke Internet (untuk demo/demo tim)
Agar teman bisa akses dari laptopnya, gunakan **ngrok** (tunnel):

```bash
# Install ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
# Atau download dari ngrok.com

# Jalankan tunnel ke port 8000
ngrok http 8000
```

Ngrok akan memberikan URL publik seperti `https://abc123.ngrok.io`. Teman Anda bisa akses URL itu dari browser mana saja.

---

### Rekomendasi untuk Tugas Ini

| Kebutuhan | Pilihan |
|---|---|
| Database bersama tim, server masih lokal | **Supabase** + ngrok |
| Paling simpel, demo cepat | **ngrok** saja (SQLite tetap lokal, tapi akses via URL publik) |
| Deploy full ke cloud | Railway / Render (gratis, deploy FastAPI + PostgreSQL sekaligus) |

Untuk tugas kuliah, **kombinasi Supabase + ngrok** adalah yang paling cepat diimplementasikan — kurang dari 10 menit. Mau saya bantu setup Supabase dan update `config.py`-nya?

### User Input

ya bantu setup, dan list yang harus saya berikan apa saja

### Planner Response

### Yang Harus Anda Sediakan

Ikuti langkah ini dulu sebelum saya ubah kodenya:

**Langkah 1 — Buat project Supabase:**
1. Buka [supabase.com](https://supabase.com) → Sign Up / Login
2. Klik **"New Project"**
3. Isi: Project Name (misal: `martabak-core`), Database Password (catat!), Region pilih `Southeast Asia (Singapore)`
4. Tunggu ~2 menit sampai project siap

**Langkah 2 — Ambil Connection String:**
1. Di dashboard Supabase → klik **Settings** (ikon gear kiri bawah)
2. Klik **Database** → scroll ke **"Connection string"**
3. Pilih tab **URI**
4. Copy string tersebut (formatnya: `postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres`)

**Langkah 3 — Berikan ke saya:**
- Connection string PostgreSQL dari Supabase (ganti `[YOUR-PASSWORD]` dengan password yang Anda buat)

---

Sementara itu, saya siapkan dulu perubahan kode yang diperlukan:

