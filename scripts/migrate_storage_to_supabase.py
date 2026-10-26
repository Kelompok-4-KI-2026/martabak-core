"""One-off migration: move vault blobs from local folders into Supabase Storage.

1. Creates the two buckets if missing (both private):
       encrypted-storage  <- encrypted_storage/*.enc
       keys               <- keys/*.key
2. Uploads every local object (upsert, idempotent). Nothing is deleted locally.
3. Rewrites vault_files.encrypted_filepath to the bare object name (basename),
   so the app can combine it with the bucket at download time.

Usage:
    env -u PYTHONPATH .venv/bin/python scripts/migrate_storage_to_supabase.py [--dry-run]

Requires SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY in the environment (or .env).
Does not alter API routes or table structure — only the encrypted_filepath values.
"""

import argparse
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import (  # noqa: E402
    BUCKET_ENCRYPTED,
    BUCKET_KEYS,
    DATABASE_URL,
    KEYS_DIR,
    STORAGE_DIR,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_URL,
    USE_SUPABASE_STORAGE,
)
from core.storage_client import SupabaseStorageClient  # noqa: E402


def ensure_bucket(client: SupabaseStorageClient, name: str, dry_run: bool) -> None:
    """Create a private bucket if it does not exist yet."""
    import httpx

    resp = httpx.get(
        f"{SUPABASE_URL}/storage/v1/bucket/{name}",
        headers=client._headers,
        timeout=30.0,
    )
    if resp.status_code == 200:
        print(f"bucket '{name}': already exists")
        return
    if dry_run:
        print(f"bucket '{name}': would create")
        return
    resp = httpx.post(
        f"{SUPABASE_URL}/storage/v1/bucket",
        headers={**client._headers, "Content-Type": "application/json"},
        json={"name": name, "public": False},
        timeout=30.0,
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"create bucket '{name}' failed: {resp.status_code} {resp.text}")
    print(f"bucket '{name}': created (private)")


def upload_folder(
    client: SupabaseStorageClient,
    bucket: str,
    folder: Path,
    dry_run: bool,
) -> tuple[int, int]:
    """Upload every file in *folder* to *bucket*. Returns (uploaded, skipped)."""
    files = sorted(p for p in folder.iterdir() if p.is_file())
    uploaded = skipped = 0
    for path in files:
        # In dry-run the buckets do not exist yet, so skip remote existence
        # checks and simply count what would be uploaded.
        if not dry_run and client.exists(bucket, path.name):
            skipped += 1
            continue
        if dry_run:
            uploaded += 1
            continue
        client.upload(bucket, path.name, path.read_bytes())
        uploaded += 1
    print(f"bucket '{bucket}': {uploaded} uploaded, {skipped} already present "
          f"({len(files)} local files in {folder})")
    return uploaded, skipped


def normalize_paths(dry_run: bool) -> int:
    """Rewrite vault_files.encrypted_filepath to basenames (idempotent)."""
    if DATABASE_URL.startswith("sqlite"):
        sys.exit("DATABASE_URL still points at SQLite - aborting.")
    engine = create_engine(DATABASE_URL)
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT id, encrypted_filepath FROM vault_files")).fetchall()
        stale = [(rid, p) for rid, p in rows if p != Path(p).name]
        if dry_run:
            print(f"vault_files: would rewrite {len(stale)} of {len(rows)} rows")
            return len(stale)
        for rid, _old in stale:
            conn.execute(
                text("UPDATE vault_files SET encrypted_filepath = :p WHERE id = :i"),
                {"p": Path(_old).name, "i": rid},
            )
    print(f"vault_files: rewrote {len(stale)} of {len(rows)} rows to bare object names")
    return len(stale)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not USE_SUPABASE_STORAGE:
        sys.exit("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set - aborting.")

    client = SupabaseStorageClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

    ensure_bucket(client, BUCKET_ENCRYPTED, args.dry_run)
    ensure_bucket(client, BUCKET_KEYS, args.dry_run)

    upload_folder(client, BUCKET_ENCRYPTED, Path(STORAGE_DIR), args.dry_run)
    upload_folder(client, BUCKET_KEYS, Path(KEYS_DIR), args.dry_run)
    normalize_paths(args.dry_run)

    if args.dry_run:
        print("dry-run: no changes written.")
    else:
        print("OK: storage migration complete (local files kept as-is)")


if __name__ == "__main__":
    main()
