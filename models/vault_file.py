from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from database import Base


class VaultFile(Base):
    __tablename__ = "vault_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    file_type = Column(String(50), nullable=False)  # personal_data, id_scan, office_doc, video
    original_filename = Column(String(255), nullable=False)
    encrypted_filepath = Column(String(500), nullable=False)
    cipher_used = Column(String(20), nullable=False)  # AES, DES, RC4
    cipher_mode = Column(String(20), nullable=False)  # CBC, STREAM
    key_id = Column(String(100), nullable=False)  # UUID key identifier in KeyManager
    iv_hex = Column(String(64), nullable=True)  # Hex representation of IV (nullable for RC4)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
