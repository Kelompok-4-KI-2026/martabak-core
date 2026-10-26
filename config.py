import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Load .env file if it exists (zero-dependency)
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))

SECRET_KEY = os.getenv("SECRET_KEY", "martabak-core-ultra-secure-secret-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

raw_db_url = os.getenv("DATABASE_URL", "sqlite:///./martabak.db").strip()
if not raw_db_url or raw_db_url.startswith("TEMPEL_") or "://" not in raw_db_url:
    raw_db_url = "sqlite:///./martabak.db"

if raw_db_url.startswith("postgres://"):
    raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
DATABASE_URL = raw_db_url

STORAGE_DIR = os.getenv("STORAGE_DIR", str(BASE_DIR / "encrypted_storage"))
KEYS_DIR = os.getenv("KEYS_DIR", str(BASE_DIR / "keys"))

os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(KEYS_DIR, exist_ok=True)
