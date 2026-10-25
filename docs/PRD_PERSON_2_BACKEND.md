# 📄 PRD 2: Backend & Database (Person 2)

* **Target Teammate:** Person 2 (Backend & Database Developer)
* **Branch to Create:** `feature/backend-api`
* **Files to Manage:** `database.py`, `models/`, `routers/auth_router.py`, `routers/vault_router.py`, `main.py`

---

### **1. Objective**

Build the FastAPI application server, database models using SQLAlchemy with PostgreSQL, and endpoints handling user authentication, metadata tracking, and secure multipart file uploads/downloads for **Martabak Core**.

### **2. Strict Technical Constraints (Assignment Rules)**

* **User Authentication & Authorization:** Only authenticated users are allowed to upload, view, and retrieve their files.


* **Strict User Isolation:** A user can *only* retrieve their own files. The backend must verify file ownership via `user_id` before serving any decrypted content.


* **Database Management:** Store user profiles and encrypted file metadata securely in PostgreSQL.

---

### **3. Implementation Blueprint**

#### **Step A: Database Connection (`database.py`)**

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/martabak_core")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```

#### **Step B: SQLAlchemy Models (`models/user.py` & `models/vault_file.py`)**

```python
# models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# models/vault_file.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from database import Base

class VaultFile(Base):
    __tablename__ = "vault_files"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_type = Column(String(50), nullable=False) # personal_data, id_scan, office_doc, video
    original_filename = Column(String(255), nullable=False)
    encrypted_filepath = Column(String(505), nullable=False)
    cipher_used = Column(String(20), nullable=False) # AES, DES, RC4
    cipher_mode = Column(String(20), nullable=False) # CBC, STREAM
    created_at = Column(DateTime, default=datetime.utcnow)

```

#### **Step C: Vault Router Integration (`routers/vault_router.py`)**

This route handles receiving files from the frontend, invoking Person 1's crypto engine, saving the binary `.enc` file locally, and saving records to PostgreSQL:

```python
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.vault_file import VaultFile
from core.cipher_engine import MartabakCipherEngine
import os
import uuid

router = APIRouter(prefix="/api/v1/vault", tags=["Vault"])
STORAGE_DIR = "encrypted_storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

@router.post("/upload")
async def upload_vault_file(
    file: UploadFile = File(...),
    file_type: str = Form(...), # e.g., id_scan, office_doc, video, personal_data
    cipher_choice: str = Form(...), # AES, DES, RC4
    db: Session = Depends(get_db)
):
    # Read file bytes
    file_bytes = await file.read()
    
    try:
        # Encrypt using Crypto Core (Person 1's engine)
        encrypted_data = MartabakCipherEngine.encrypt_data(file_bytes, cipher_choice)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Encryption failed: {str(e)}")
    
    # Save encrypted payload to disk
    file_id_name = f"{uuid.uuid4()}.enc"
    file_path = os.path.join(STORAGE_DIR, file_id_name)
    with open(file_path, "wb") as f:
        f.write(encrypted_data["ciphertext"])
        
    # Save metadata to PostgreSQL (hardcoded user_id=1 for initial MVP test)
    db_file = VaultFile(
        user_id=1, 
        file_type=file_type,
        original_filename=file.filename,
        encrypted_filepath=file_path,
        cipher_used=cipher_choice.upper(),
        cipher_mode=encrypted_data["mode"]
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return {
        "status": "success",
        "file_id": db_file.id,
        "message": f"Successfully encrypted with {cipher_choice.upper()} and stored securely."
    }

```

---

### **4. Acceptance Criteria (Definition of Done)**

* [ ] FastAPI server starts successfully (`uvicorn main:app --reload`).
* [ ] Database tables (`users`, `vault_files`) migrate and initialize correctly in PostgreSQL.
* [ ] POST `/api/v1/vault/upload` successfully accepts multipart files, processes them, saves the `.enc` block to disk, and commits metadata to the database.
* [ ] Atomic git commits made during feature development.