import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required and must not be empty.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required and must not be empty.")

STORAGE_DIR = os.getenv("STORAGE_DIR", str(BASE_DIR / "encrypted_storage"))
KEYS_DIR = os.getenv("KEYS_DIR", str(BASE_DIR / "keys"))

# ---------------------------------------------------------------------------
# Supabase Storage (production / Vercel)
# ---------------------------------------------------------------------------
# When both are set, encrypted payloads and keys live in Supabase Storage
# buckets instead of local folders. On Vercel the filesystem is read-only,
# so local folders must never be created or written to.
SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.getenv(
    "SUPABASE_SERVICE_ROLE_KEY", os.getenv("SUPABASE_KEY", "")
)

USE_SUPABASE_STORAGE = bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY)

# Bucket names (must exist in the Supabase project)
BUCKET_ENCRYPTED = os.getenv("SUPABASE_BUCKET_ENCRYPTED", "encrypted-storage")
BUCKET_KEYS = os.getenv("SUPABASE_BUCKET_KEYS", "keys")

if not USE_SUPABASE_STORAGE:
    # Local development / test fallback only.
    os.makedirs(STORAGE_DIR, exist_ok=True)
    os.makedirs(KEYS_DIR, exist_ok=True)
