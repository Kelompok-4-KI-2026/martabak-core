from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class VaultFileOut(BaseModel):
    id: int
    user_id: int
    file_type: str
    original_filename: str
    cipher_used: str
    cipher_mode: str
    file_size: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class VaultUploadResponse(BaseModel):
    status: str
    file_id: int
    message: str
    original_filename: str
    cipher_used: str
    cipher_mode: str
