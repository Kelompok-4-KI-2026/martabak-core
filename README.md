
# 🍫 Martabak Core: The Franchise Secret Recipe & Merchant Vault

> *"Because your chocolate-peanut ratio is trade secret, and your franchisee's KTP scan shouldn't leak onto a public server."*

---

## What is this project?
Welcome to **Martabak Core**—a production-ready, hyper-secure web application built for a high-turnover culinary franchise. 

Behind the casual name, this system is engineered to solve a serious real-world problem: **how to securely store, encrypt, and manage sensitive merchant data and proprietary trade secrets** while complying strictly with modern data protection regulations (such as **UU PDP and GDPR**). 

*Spoiler alert: Whether this ends up running a real family martabak empire someday, or just serves as proof that you can build a bulletproof vault from scratch when someone says "we hired a contractor," Martabak Core gets the job done.*

---

## How We Solved the Assignment Requirements (`Tugas 1`)

To satisfy our university cryptography assignment, every single requirement from the prompt is hardcoded into our architecture:

1. **Concrete Scenario & Data Categories:** 
   We chose a franchise merchant portal where users handle four mandatory data types:
   * **Personal Data:** Franchisee full name, phone number, and bank account details.
   * **Identity Document Scans:** Scanned KTP and NPWP documents.
   * **Office Documents:** The proprietary, highly confidential **Secret Batter & Topping Formula PDF**.
   * **Videos:** High-definition kitchen SOP and dough-folding masterclass videos.
2. **Privacy Law Alignment (UU PDP / GDPR):** 
   Under data privacy legislation, unencrypted PII and commercial trade secrets expose businesses to massive legal liability. Martabak Core enforces zero-knowledge storage principles.
3. **The Three Ciphers (`AES`, `DES`, `RC4`):** 
   We implemented all three algorithms natively using `pycryptodome`.
4. **Strict Authentication & Zero-Leak Retrieval:** 
   Only authenticated users can fetch their own encrypted files. The backend enforces strict user-ID isolation checks so nobody can peek at another merchant's recipe files.

---

## Cryptography & Security Architecture

* **No ECB Mode Allowed:** Electronic Codebook (ECB) mode leaves visual patterns visible in encrypted data. We strictly use secure block modes like **CBC (Cipher Block Chaining)** with randomized IVs and **RC4** stream ciphers.
* **Integrity Guarantee:** Decryption routines ensure that files return 100% intact (zero binary corruption upon retrieval).

---

## System Architecture & Tech Stack

We built this entirely on a lightweight, lightning-fast **100% Python Stack**:
* **Backend:** FastAPI (Automatic documentation, seamless async handling).
* **Database & ORM:** PostgreSQL + SQLAlchemy (Robust relational user and metadata storage).
* **Frontend:** Jinja2 Templates + Tailwind CSS via CDN (Clean, responsive UI with zero heavy JavaScript bundling overhead).
* **Crypto Engine:** Python `pycryptodome`.

```text
 [ Franchisee Client Browser ] 
              │ (Multipart Upload / Auth Token)
              ▼
    [ FastAPI Application Server ]
      ├── Auth & Session Guards (User Isolation)
      ├── File Type Validator (Personal Data, ID Scans, PDFs, Videos)
      └── Crypto Core Engine ──► [ AES / DES / RC4 Execution ]
                                          │
            ┌─────────────────────────────┴─────────────────────────────┐
            ▼                                                           ▼
   [ PostgreSQL Database ]                                    [ Local Encrypted Vault ]
   (User Metadata & Cipher Logs)                              (/encrypted_storage/*.enc)

```

---

## Quick Start Guide (For the Squad)

If you want to run this locally on your machine, follow these steps:

1. **Clone and enter the repository:**
```bash
git clone [https://github.com/Kelompok-4-KI-2026/martabak-core.git](https://github.com/Kelompok-4-KI-2026/martabak-core.git)
cd martabak-core

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the FastAPI server:**
```bash
uvicorn main:app --reload

```


4. **Explore the interactive API docs:**
Open your browser and navigate to `http://127.0.0.1:8000/docs` to test endpoints directly via Swagger UI.

---

## Performance Benchmark & Evaluation

Our evaluation runner (`benchmarks/runner.py`) measures encryption/decryption speeds and throughput across varying file sizes (from small 1KB text PII strings to heavy 5MB SOP videos).

The detailed performance metrics, graphs, and human analysis are compiled directly into our final 2-page A4 report, interpreting why modern AES-256-CBC outperforms legacy DES and why RC4 stream ciphers behave differently in practice.
