import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.getenv("SECRET_KEY", "martabak-core-ultra-secure-secret-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./martabak.db")

STORAGE_DIR = os.getenv("STORAGE_DIR", str(BASE_DIR / "encrypted_storage"))
KEYS_DIR = os.getenv("KEYS_DIR", str(BASE_DIR / "keys"))

os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(KEYS_DIR, exist_ok=True)
