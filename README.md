<div align="center">

# Martabak Core

### The Franchise Secret Recipe &amp; Merchant Vault

*Because your chocolate-peanut ratio is a trade secret, and your franchisee's KTP scan shouldn't leak onto a public server.*

<br/>

[![Python](https://img.shields.io/badge/Python-3.12-1a1a1a?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-1a1a1a?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Postgres%20%2B%20Storage-1a1a1a?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployment-1a1a1a?style=flat-square&logo=vercel&logoColor=white)](https://martabak-core.vercel.app)
[![PyCryptodome](https://img.shields.io/badge/Crypto-pycryptodome-1a1a1a?style=flat-square)](https://pypi.org/project/pycryptodome/)

<br/>

**[ Live Demo ](https://martabak-core.vercel.app)**&ensp;·&ensp;**[ API Documentation ](https://martabak-core.vercel.app/docs)**&ensp;·&ensp;**[ Repository ](https://github.com/Kelompok-4-KI-2026/martabak-core)**

</div>

---

<details>
<summary><b>Table of Contents</b></summary>

- [Overview](#overview)
- [Assignment Requirements](#assignment-requirements)
- [Cryptography & Security](#cryptography--security)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Benchmark](#benchmark)
- [Team](#team)

</details>

---

<a id="overview"></a>

## Overview

**Martabak Core** is a production-ready, hyper-secure web application built for a high-turnover culinary franchise. Behind the casual name, this system solves a serious real-world problem: **how to securely store, encrypt, and manage sensitive merchant data and proprietary trade secrets** while complying strictly with modern data protection regulations (**UU PDP &amp; GDPR**).

Files are encrypted before storage (AES-256-CBC / DES-CBC / RC4), ciphertext lives in **private Supabase Storage buckets**, keys are kept in a **separate isolated bucket**, and only metadata touches the database — so even a full database dump yields nothing but opaque blobs.

> Try it now: **[martabak-core.vercel.app](https://martabak-core.vercel.app)** — register an account, upload a file, and inspect the ciphertext yourself.

---

<a id="assignment-requirements"></a>

## Assignment Requirements

Every requirement of the cryptography assignment is enforced in our architecture:

1. **Concrete Scenario &amp; Data Categories** — Franchise merchant portal supporting four data types:
   * **Personal Data:** Franchisee full name, phone number, and agreement details.
   * **Identity Document Scans:** Scanned KTP and NPWP documents.
   * **Office Documents:** Confidential recipe formulas and operational standards.
   * **Videos:** Masterclass kitchen SOP and dough preparation training videos.
2. **Privacy Law Alignment (UU PDP / GDPR)** — Unencrypted PII and commercial trade secrets expose businesses to massive legal liability. Martabak Core enforces zero-knowledge storage principles.
3. **The Three Ciphers (`AES-256-CBC`, `DES-CBC`, `RC4`)** — Implemented natively using `pycryptodome`, strictly avoiding ECB mode.
4. **Strict Authentication &amp; Multi-Tenant Isolation** — Only authenticated users can access their own encrypted files. The backend enforces user-level isolation checks.
5. **Ciphertext Inspector &amp; Avalanche Effect** — Built-in cryptographic inspector displaying real-time Shannon entropy (*H* ≤ 8.00), block segmentation mapping, IEEE 802/POSIX hex dump, and live avalanche effect (bit diffusion) analysis.

---

<a id="cryptography--security"></a>

## Cryptography &amp; Security

* **No ECB Mode Allowed** — Electronic Codebook (ECB) leaves visual patterns visible in encrypted data. We strictly enforce **CBC (Cipher Block Chaining)** with randomized IVs for block ciphers and **RC4** stream ciphers.
* **Integrity Guarantee** — Decryption routines ensure that files return 100% intact, with zero binary corruption upon retrieval.
* **Key Management** — Cryptographic keys are generated with `os.urandom` and stored in an **isolated, private `keys` bucket** per asset — physically separated from ciphertext.
* **Path-Traversal Protection** — All storage object names are sanitized to basenames before touching any storage backend.
* **Secrets Discipline** — `SECRET_KEY` and `DATABASE_URL` have **no defaults**; the app refuses to boot without them. `.env` is git-ignored and never shipped to the deployment bundle.

---

<a id="architecture--tech-stack"></a>

## Architecture &amp; Tech Stack

| Layer | Technology |
|:--|:--|
| Backend | **FastAPI** — Python 3.12, async, automatic OpenAPI docs |
| Database &amp; ORM | **PostgreSQL** (Supabase cloud pooler) via SQLAlchemy + `psycopg2-binary` |
| Encrypted Blob Storage | **Supabase Storage** — private buckets `encrypted-storage` (ciphertext) and `keys` (per-file keys) |
| Frontend | **Jinja2 Templates** + Tailwind CSS (CDN) + typography trio — *Young Serif*, *Schibsted Grotesk*, *Martian Mono* |
| Crypto Engine | **pycryptodome** — AES-256-CBC, DES-CBC, RC4 |
| Hosting | **Vercel** — serverless Python runtime, read-only filesystem |
| Configuration | **python-dotenv** with strict environment-variable enforcement |

```text
 [ Franchisee Client Browser ]
              │ (Multipart Upload / Auth Cookie)
              ▼
     [ FastAPI on Vercel ]  ← api/index.py entrypoint
       ├── Auth & Session Guards (User Isolation)
       ├── File Type Validator (Personal Data, ID Scans, PDFs, Videos)
       └── Crypto Core Engine ──► [ AES / DES / RC4 Execution ]
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            ▼                             ▼                             ▼
 [ PostgreSQL (Supabase) ]   [ Storage: encrypted-storage ]   [ Storage: keys ]
 (users & vault_files meta)      (*.enc ciphertext blobs)      (*.key isolated)
```

The Vercel filesystem is **read-only and ephemeral** — the application performs zero local disk I/O in production. Every byte goes through Supabase REST APIs.

---

<a id="getting-started"></a>

## Getting Started

**Prerequisites:** Python 3.12+, `git`, and a free [Supabase](https://supabase.com/) project.

### Option 1 — Run Locally

```bash
# 1. Clone and enter the repository
git clone https://github.com/Kelompok-4-KI-2026/martabak-core.git
cd martabak-core

# 2. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Create your .env (see Configuration below)
cp .env.example .env   # never commit this file

# 4. Run the FastAPI server
uvicorn main:app --reload --port 8000
```

| Page | URL |
|:--|:--|
| Web Portal (Login) | http://127.0.0.1:8000/login |
| Interactive API Docs (Swagger) | http://127.0.0.1:8000/docs |
| Health Check | http://127.0.0.1:8000/health |

### Option 2 — Run with Docker

Persistent volumes for local-mode keys and encrypted files:

```bash
docker-compose up --build -d   # build and start
docker-compose logs -f         # follow logs
```

The application will be accessible at `http://localhost:8000`.

---

<a id="configuration"></a>

## Configuration

Create a `.env` in the project root (never commit it — it is git-ignored):

```env
# Supabase PostgreSQL Connection String (REQUIRED — no default)
DATABASE_URL="postgresql://postgres.<PROJECT_REF>:<DB_PASSWORD>@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres"

# Application Secret Key for session signing (REQUIRED — no default, use a long random string)
SECRET_KEY="your-strong-random-secret-key"

# Supabase Storage credentials — enables remote storage mode
SUPABASE_URL="https://<PROJECT_REF>.supabase.co"
SUPABASE_SERVICE_ROLE_KEY="<SERVICE_ROLE_KEY>"

# Optional tuning
ACCESS_TOKEN_EXPIRE_MINUTES="120"
```

| Variable | Required | Default | Purpose |
|:--|:--:|:--|:--|
| `SECRET_KEY` | Yes | — | Session signing. The app refuses to boot if empty. |
| `DATABASE_URL` | Yes | — | Supabase Postgres pooler connection string. |
| `SUPABASE_URL` | Either* | — | With the service-role key, switches storage to Supabase buckets. |
| `SUPABASE_SERVICE_ROLE_KEY` | Either* | — | Server-side key for the Storage REST API (alias: `SUPABASE_KEY`). |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `120` | Session lifetime. |
| `SUPABASE_BUCKET_ENCRYPTED` | No | `encrypted-storage` | Ciphertext bucket name. |
| `SUPABASE_BUCKET_KEYS` | No | `keys` | Key vault bucket name. |
| `STORAGE_DIR` / `KEYS_DIR` | No | `./encrypted_storage`, `./keys` | Local fallback directories (dev and tests only). |

\* If `SUPABASE_URL` and the service-role key are both set, files go to the two **private** Supabase buckets. Without them, the application falls back to local directories — convenient for offline tests; production must use Supabase.

---

<a id="deployment"></a>

## Deployment

The application is deployed at **[martabak-core.vercel.app](https://martabak-core.vercel.app)** via the Vercel serverless Python runtime.

**What we ship:**

* `api/index.py` — serverless entrypoint that mounts the FastAPI `app`.
* `vercel.json` — routes all traffic to the entrypoint via `@vercel/python`.
* `.vercelignore` — strips `.env`, local blobs, databases, and tests from the deployment bundle.

**Vercel Project → Settings → Environment Variables** (set for both *Production* and *Preview*):

| Variable | Value |
|:--|:--|
| `SECRET_KEY` | a long random string |
| `DATABASE_URL` | Supabase Postgres pooler URI |
| `SUPABASE_URL` | `https://<PROJECT_REF>.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service-role key |

**Supabase setup:**

1. Two **private** buckets: `encrypted-storage` (ciphertext) and `keys` (per-file keys).
2. Tables `users` and `vault_files` live in Postgres — metadata only, never plaintext.
3. Migrating an existing local vault? Use `scripts/migrate_storage_to_supabase.py` (idempotent, supports `--dry-run`).

Deploy from your machine with the Vercel CLI:

```bash
vercel --prod
```

---

<a id="testing"></a>

## Testing

```bash
env -u PYTHONPATH .venv/bin/python -m pytest -p no:launch_testing
```

The suite of 45 tests covers the crypto engine, key manager, storage client (local &amp; Supabase), auth isolation, and the full upload → encrypt → store → download → decrypt round-trip.

---

<a id="project-structure"></a>

## Project Structure

```text
martabak-core/
├── main.py                  # FastAPI app + web portal routes
├── config.py                # .env loading & strict validation
├── core/                    # crypto engine, key manager, storage client
├── routers/                 # API routers (auth, vault)
├── templates/               # Jinja2 frontend
├── api/index.py             # Vercel serverless entrypoint
├── scripts/                 # DB & storage migration helpers
├── tests/                   # pytest suite
├── benchmarks/              # encryption throughput evaluation
└── vercel.json              # Vercel deployment config
```

---

<a id="benchmark"></a>

## Benchmark

<details>
<summary>Details</summary>

The evaluation runner (`benchmarks/runner.py`) measures encryption and decryption speed and throughput across varying file sizes — from small 1 KB text PII strings to heavy 5 MB SOP videos.

</details>

---

<a id="team"></a>

## Team

Built by **Kelompok 4** — Keamanan Informasi 2026.

**[github.com/Kelompok-4-KI-2026/martabak-core](https://github.com/Kelompok-4-KI-2026/martabak-core)**

<div align="center">
<sub>Martabak Core — secret recipes deserve real cryptography.</sub>
</div>
