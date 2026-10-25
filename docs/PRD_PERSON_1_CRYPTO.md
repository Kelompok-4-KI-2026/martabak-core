# 📄 PRD 1: Cryptography & Security Core (Person 1)

* **Target Teammate:** Person 1 (Security & Crypto Specialist)
* **Branch to Create:** `feature/crypto-engine`
* **File to Create:** `core/cipher_engine.py` and `core/key_manager.py`

---

### **1. Objective**

Implement the cryptographic engine for **Martabak Core** using Python (`pycryptodome`). This module must securely encrypt and decrypt four required data types (personal data, identity document scans, office documents, and videos) using **AES, DES, and RC4**.

### **2. Strict Technical Constraints (Assignment Rules)**

* **No ECB Mode:** Electronic Codebook (ECB) mode is strictly prohibited. You **must** use secure block cipher modes of operation such as **CBC** (Cipher Block Chaining) or **CTR** with proper IV/Nonce management.


* **Data Integrity:** Decryption must return the file **100% intact** (exact binary match with the original uploaded file, with zero corruption).


* **Cipher Support:** Must explicitly support and implement all three requested ciphers:


1. **AES** (e.g., AES-256 in CBC mode with PKCS7 padding)
2. **DES** (e.g., DES in CBC mode with proper key/IV handling)
3. **RC4** (Stream cipher implementation)



---

### **3. Implementation Blueprint (`core/cipher_engine.py`)**

Give this code structure to Person 1 (or let their AI assistant implement it based on these exact specifications):

```python
from Crypto.Cipher import AES, DES, ARC4
from Crypto.Util.Padding import pad, unpad
import os

class MartabakCipherEngine:
    """
    Core encryption and decryption engine supporting AES, DES, and RC4.
    Strictly enforces non-ECB block cipher modes (CBC).
    """
    
    @staticmethod
    def encrypt_data(file_bytes: bytes, cipher_type: str) -> dict:
        """
        Encrypts raw file bytes using the specified cipher.
        Returns ciphertext bytes along with necessary IV/Nonce metadata.
        """
        cipher_type = cipher_type.upper()
        
        if cipher_type == "AES":
            key = os.urandom(32) # 256-bit key
            cipher = AES.new(key, AES.MODE_CBC)
            ciphertext = cipher.encrypt(pad(file_bytes, AES.block_size))
            return {
                "ciphertext": ciphertext,
                "key": key,
                "iv": cipher.iv,
                "mode": "CBC"
            }
            
        elif cipher_type == "DES":
            key = os.urandom(8) # 64-bit key for DES
            cipher = DES.new(key, DES.MODE_CBC)
            ciphertext = cipher.encrypt(pad(file_bytes, DES.block_size))
            return {
                "ciphertext": ciphertext,
                "key": key,
                "iv": cipher.iv,
                "mode": "CBC"
            }
            
        elif cipher_type == "RC4":
            key = os.urandom(16) # RC4 key stream
            cipher = ARC4.new(key)
            ciphertext = cipher.encrypt(file_bytes)
            return {
                "ciphertext": ciphertext,
                "key": key,
                "iv": None, # RC4 doesn't use IV
                "mode": "STREAM"
            }
        else:
            raise ValueError(f"Unsupported cipher type: {cipher_type}")

    @staticmethod
    def decrypt_data(ciphertext: bytes, key: bytes, cipher_type: str, iv: bytes = None) -> bytes:
        """
        Decrypts ciphertext back to original raw bytes ensuring 100% integrity.
        """
        cipher_type = cipher_type.upper()
        
        if cipher_type == "AES":
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            return unpad(cipher.decrypt(ciphertext), AES.block_size)
            
        elif cipher_type == "DES":
            cipher = DES.new(key, DES.MODE_CBC, iv=iv)
            return unpad(cipher.decrypt(ciphertext), DES.block_size)
            
        elif cipher_type == "RC4":
            cipher = ARC4.new(key)
            return cipher.decrypt(ciphertext)
        else:
            raise ValueError(f"Unsupported cipher type: {cipher_type}")

```

---

### **4. Acceptance Criteria (Definition of Done)**

* [ ] Code runs without throwing padding or key-size errors.
* [ ] Successfully encrypts and decrypts a test file (e.g., a PDF or image) using AES, DES, and RC4 with identical output checksums.
* [ ] Atomic git commits made during development (e.g., *"feat: implement AES-CBC encryption"*, *"feat: add RC4 stream handling"*).