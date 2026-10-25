# 📄 PRD 4: Benchmark Evaluator & Technical Writer (Person 4)

* **Target Teammate:** Person 4 (Benchmark Analyst & Technical Writer)
* **Branch to Create:** `feature/benchmark-and-docs`
* **Files to Manage:** `benchmarks/runner.py`, `benchmarks/report_data.json`, and the final 2-Page A4 Report document.



---

### **1. Objective**

Run the performance benchmarks comparing **AES, DES, and RC4** across different file types (e.g., heavy SOP video vs. light recipe PDF), analyze what the metrics mean for the **Martabak Core** franchise scenario, and write the required **2-page A4 evaluation report**.

### **2. Strict Technical Constraints (Assignment Rules)**

* **Beyond Raw Numbers:** Do not just present raw numbers in tables; you *must* interpret what the results mean for real-world franchise data privacy and security trade-offs.


* **Report Length:** Maximum **2 pages A4**.


* **AI Interaction Log:** Must compile screenshots and chat links showing how AI tools were used during development.



---

### **3. Implementation Blueprint**

#### **Step A: Automated Benchmark Runner (`benchmarks/runner.py`)**

This script tests encryption/decryption execution speed and throughput for all three ciphers across varying data sizes:

```python
import time
import json
from core.cipher_engine import MartabakCipherEngine

def run_benchmarks():
    # Simulate test data of different sizes (Small text vs Heavy Video/PDF)
    test_payloads = {
        "Small PII Data (1 KB)": b"A" * 1024,
        "Medium Office Doc (500 KB)": b"B" * (500 * 1024),
        "Heavy SOP Video (5 MB)": b"C" * (5 * 1024 * 1024)
    }
    
    ciphers = ["AES", "DES", "RC4"]
    results = {}

    for label, data in test_payloads.items():
        results[label] = {}
        for cipher in ciphers:
            # Measure Encryption Time
            start_time = time.perf_counter()
            encrypted = MartabakCipherEngine.encrypt_data(data, cipher)
            enc_time = (time.perf_counter() - start_time) * 1000 # in ms
            
            # Measure Decryption Time
            start_time = time.perf_counter()
            MartabakCipherEngine.decrypt_data(
                encrypted["ciphertext"], 
                encrypted["key"], 
                cipher, 
                encrypted.get("iv")
            )
            dec_time = (time.perf_counter() - start_time) * 1000 # in ms
            
            results[label][cipher] = {
                "encryption_ms": round(enc_time, 3),
                "decryption_ms": round(dec_time, 3)
            }
            print(f"[{label}] {cipher} -> Enc: {enc_time:.2f}ms | Dec: {dec_time:.2f}ms")

    # Save output for report inclusion
    with open("benchmarks/report_data.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\nBenchmarks completed successfully. Results saved to report_data.json.")

if __name__ == "__main__":
    run_benchmarks()

```

---

#### **Step B: Structure for the 2-Page A4 Report**



Person 4 should structure the final written report into these 4 concise sections:

1. **Scenario & Business Value:**
* Introduce **Martabak Core** (Franchise Secret Recipe & Merchant Vault) and explain why protecting franchisee KTP scans, financial reports, and kitchen SOP videos is vital under data privacy laws (GDPR / UU PDP).




2. **Architectural & Design Justifications:**
* Explain why FastAPI and PostgreSQL were chosen, and justify why non-ECB block cipher modes (CBC) were enforced over insecure alternatives.




3. **Cipher Evaluation & Analysis:**
* Insert the benchmark metrics from `report_data.json`. Interpret the trade-offs (e.g., why DES is slower and insecure despite legacy status, why RC4 is fast but deprecated, and why AES-256-CBC offers the optimal balance of speed and cryptographic security).




4. **AI Usage Disclosure & Logs:**
* Provide the required links and screenshots documenting how AI assistance was leveraged and verified during the project.





---

### **4. Acceptance Criteria (Definition of Done)**

* [ ] Benchmark script executes cleanly (`python benchmarks/runner.py`) and generates `report_data.json`.
* [ ] Final 2-page A4 report draft is compiled, addressing all assignment criteria with human interpretation.


* [ ] AI interaction logs and screenshots are packaged for submission.