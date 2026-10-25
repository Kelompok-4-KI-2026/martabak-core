# 🤖 AI Agent Engineering Protocols for Martabak Core

## 🚨 MANDATORY RULES FOR ALL AI ASSISTANTS (Cursor, Claude, ChatGPT, etc.)
You are assisting university students in building a secure Python/FastAPI cryptography web application ("Martabak Core"). The team is graded strictly on **clean architectural contracts** and **meaningful, routine Git commit history**. Bulk code dumping or unverified code generation is strictly prohibited[cite: 1].

### Rule 1: Atomic, Incremental Development
- **NEVER** write the entire application or multiple unrelated modules in a single response or file generation.
- Break every task down into micro-steps: build one function, test it, verify it, and prompt the human to commit it (`git commit -m "feat(module): description"`) before moving to the next line of code.

### Rule 2: Strict Adherence to API & Data Contracts
- Do not modify database schemas, endpoint paths, request parameters, or response JSON payloads unless explicitly authorized by the team lead.
- Keep data isolation intact: Users can only query, download, and decrypt files belonging to their own `user_id`[cite: 1].

### Rule 3: Cryptography Constraints (No ECB Mode!)
- When implementing AES, DES, or RC4 in `core/cipher_engine.py`, **ECB mode is strictly forbidden** per project requirements[cite: 1]. Always use secure block modes like CBC, CTR, or GCM with proper IV/Nonce handling.
- Ensure decrypted files return **100% intact** without data corruption[cite: 1].

### Rule 4: Human-in-the-Loop Verification
- Before finishing any task, the AI must output a short checklist for the student verifying:
  1. Does this code match the contract?
  2. Is it safe to commit this single file/module now?