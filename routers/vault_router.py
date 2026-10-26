import os
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from config import KEYS_DIR, STORAGE_DIR
from core.auth_security import get_current_user
from core.cipher_engine import MartabakCipherEngine
from core.inspector import inspect_vault_payload
from core.key_manager import KeyManager
from database import get_db
from models.user import User
from models.vault_file import VaultFile
from schemas.vault_schema import VaultFileOut, VaultUploadResponse

router = APIRouter(prefix="/api/v1/vault", tags=["Vault"])

ALLOWED_FILE_TYPES = {"personal_data", "id_scan", "office_doc", "video"}
ALLOWED_CIPHERS = {"AES", "DES", "RC4"}


@router.post("/upload", response_model=VaultUploadResponse)
async def upload_vault_file(
    request: Request,
    file: UploadFile = File(...),
    file_type: str = Form(...),
    cipher_choice: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cipher_clean = cipher_choice.strip().upper()
    if cipher_clean not in ALLOWED_CIPHERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported cipher '{cipher_choice}'. Supported: {', '.join(ALLOWED_CIPHERS)}",
        )

    if file_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file_type}'. Supported: {', '.join(ALLOWED_FILE_TYPES)}",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    try:
        # Encrypt via Cryptography Core Engine
        encrypted_result = MartabakCipherEngine.encrypt_data(file_bytes, cipher_clean)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Encryption failed: {str(e)}",
        )

    # Persist secret key safely via KeyManager
    key_id = str(uuid.uuid4())
    KeyManager.save_key(encrypted_result["key"], key_id, keys_dir=Path(KEYS_DIR))

    # Persist encrypted payload (.enc) to vault storage
    enc_filename = f"{uuid.uuid4()}.enc"
    enc_path = os.path.join(STORAGE_DIR, enc_filename)
    with open(enc_path, "wb") as f:
        f.write(encrypted_result["ciphertext"])

    iv_hex = encrypted_result["iv"].hex() if encrypted_result.get("iv") else None

    # Persist metadata to database
    db_file = VaultFile(
        user_id=current_user.id,
        file_type=file_type,
        original_filename=file.filename or "unknown_file",
        encrypted_filepath=enc_path,
        cipher_used=cipher_clean,
        cipher_mode=encrypted_result["mode"],
        key_id=key_id,
        iv_hex=iv_hex,
        file_size=len(file_bytes),
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    # If submitted from browser form without expecting json, redirect smoothly
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header and "application/json" not in accept_header:
        return RedirectResponse(
            url=f"/?uploaded=1&file={db_file.original_filename}&cipher={cipher_clean}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return VaultUploadResponse(
        status="success",
        file_id=db_file.id,
        message=f"File encrypted with {cipher_clean} and stored securely.",
        original_filename=db_file.original_filename,
        cipher_used=db_file.cipher_used,
        cipher_mode=db_file.cipher_mode,
    )


@router.get("/files", response_model=List[VaultFileOut])
def list_user_files(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Strict User Isolation: only fetch files belonging to current authenticated user
    files = (
        db.query(VaultFile)
        .filter(VaultFile.user_id == current_user.id)
        .order_by(VaultFile.created_at.desc())
        .all()
    )
    return files


@router.get("/download/{file_id}")
def download_decrypted_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Strict User Isolation check
    file_record = (
        db.query(VaultFile)
        .filter(VaultFile.id == file_id, VaultFile.user_id == current_user.id)
        .first()
    )

    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found or access denied.",
        )

    if not os.path.exists(file_record.encrypted_filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encrypted storage file is missing.",
        )

    with open(file_record.encrypted_filepath, "rb") as f:
        ciphertext = f.read()

    try:
        # Load key from KeyManager
        key = KeyManager.load_key(file_record.key_id, keys_dir=Path(KEYS_DIR))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to retrieve encryption key: {str(e)}",
        )

    iv = bytes.fromhex(file_record.iv_hex) if file_record.iv_hex else None

    try:
        # Decrypt ciphertext back to original binary bytes
        decrypted_bytes = MartabakCipherEngine.decrypt_data(
            ciphertext=ciphertext,
            key=key,
            cipher_type=file_record.cipher_used,
            iv=iv,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Decryption failed: {str(e)}",
        )

    # Serve raw decrypted binary file
    safe_filename = Path(file_record.original_filename).name
    return Response(
        content=decrypted_bytes,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{safe_filename}"',
            "X-Cipher-Used": file_record.cipher_used,
            "X-File-Type": file_record.file_type,
        },
    )


@router.get("/{file_id}/inspect")
def inspect_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Strict User Isolation check
    file_record = (
        db.query(VaultFile)
        .filter(VaultFile.id == file_id, VaultFile.user_id == current_user.id)
        .first()
    )

    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found or access denied.",
        )

    if not os.path.exists(file_record.encrypted_filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Encrypted storage file is missing.",
        )

    with open(file_record.encrypted_filepath, "rb") as f:
        ciphertext = f.read()

    try:
        key = KeyManager.load_key(file_record.key_id, keys_dir=Path(KEYS_DIR))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to retrieve encryption key: {str(e)}",
        )

    report = inspect_vault_payload(file_record, ciphertext, key)
    return report


@router.delete("/files/{file_id}")
def delete_vault_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_record = (
        db.query(VaultFile)
        .filter(VaultFile.id == file_id, VaultFile.user_id == current_user.id)
        .first()
    )

    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found or access denied.",
        )

    # Clean up disk file
    if os.path.exists(file_record.encrypted_filepath):
        try:
            os.remove(file_record.encrypted_filepath)
        except OSError:
            pass

    # Clean up key file
    try:
        KeyManager.delete_key(file_record.key_id, keys_dir=Path(KEYS_DIR))
    except Exception:
        pass

    db.delete(file_record)
    db.commit()

    return {"status": "success", "message": "File deleted from vault."}
