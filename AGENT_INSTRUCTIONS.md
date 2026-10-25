# AI Agent Operational Rules & Team Guidelines (Martabak Core)

You are an expert AI coding assistant collaborating with a 4-person student team building "Martabak Core" under strict 2-day delivery constraints. 

## 🚨 MANDATORY EXECUTION RULES FOR AI AGENTS:
1. **Never write the whole project at once.** Build files or functions one at a time. Do not dump massive unverified code blocks.
2. **Strict Contract Adherence:** Do not alter API JSON schemas, route paths, or database structures defined in the project architecture without explicit human approval.
3. **Branch Discipline:** Remind the user to code inside a feature branch (e.g., `feature/crypto-aes`, `feature/backend-auth`, `feature/frontend-ui`, `feature/benchmark-runner`) and never push raw code straight to `main` until tested and reviewed.
4. **Atomic Commits:** Structure your code suggestions so the user can make small, frequent, meaningful git commits (vital for grading).

---

## 👥 TEAM ROLE DIRECTORIES & TASKS

### **Person 1: Cryptography & Security Specialist (`core/`)**
* Implement **AES, DES, and RC4** using `pycryptodome`[cite: 1].
* **Strict Rule:** **No ECB mode allowed** (use CBC or CTR with proper IV/Nonce handling)[cite: 1].
* Ensure full data integrity on decryption (files must return 100% intact)[cite: 1].

### **Person 2: Backend & Database Developer (`routers/`, `models/`, `database.py`)**
* Build FastAPI routes with strict authentication (users can only access their own uploaded files)[cite: 1].
* Manage PostgreSQL connection via SQLAlchemy.
* Handle multipart file uploads (`personal_data`, `id_scan`, `office_doc`, `video`)[cite: 1].

### **Person 3: Frontend & UI/UX Developer (`templates/`, `static/`)**
* Build clean, responsive Jinja2 templates styled with Tailwind CSS via CDN.
* Create intuitive dashboards for uploading franchise documents and downloading decrypted files[cite: 1].

### **Person 4: Benchmark Evaluator & Technical Writer (`benchmarks/`, Report)**
* Write the performance runner script measuring encryption/decryption speeds, memory overhead, and throughput across AES, DES, and RC4[cite: 1].
* Compile raw metrics into `benchmarks/report_data.json` to feed the **2-page A4 report**[cite: 1].
* Document AI interaction logs and screenshots as required by submission guidelines[cite: 1].