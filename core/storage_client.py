"""
core/storage_client.py
======================
Object storage layer for Martabak Core.

Two interchangeable backends behind one interface:

* ``SupabaseStorageClient`` — talks to Supabase Storage over its REST API
  (used in production, e.g. on Vercel where the filesystem is read-only).
* ``LocalStorageClient``  — writes to local folders (dev/test fallback).

``get_storage()`` picks the backend from the environment:

* ``SUPABASE_URL`` + ``SUPABASE_SERVICE_ROLE_KEY`` set  -> Supabase buckets
* otherwise                                            -> local folders

Object names are sanitised (basename only) everywhere so a malicious value
in ``vault_files.encrypted_filepath`` can never traverse directories.

Buckets used (created by scripts/migrate_storage_to_supabase.py):

* ``encrypted-storage`` -> ``*.enc`` ciphertext payloads
* ``keys``              -> ``*.key`` secret key files
"""

from pathlib import Path

import httpx

from config import (
    BUCKET_ENCRYPTED,
    BUCKET_KEYS,
    KEYS_DIR,
    STORAGE_DIR,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_URL,
    USE_SUPABASE_STORAGE,
)

# Re-export bucket names for callers.
__all__ = [
    "BUCKET_ENCRYPTED",
    "BUCKET_KEYS",
    "LocalStorageClient",
    "SupabaseStorageClient",
    "get_storage",
    "sanitize_object_name",
]

_HTTP_TIMEOUT = 30.0
_RETRIES = 3


def sanitize_object_name(name: str) -> str:
    """Return a safe object name: basename only, no empty names."""
    safe = Path(name).name
    if not safe or safe in {".", ".."}:
        raise ValueError(f"Invalid object name: {name!r}")
    return safe


class SupabaseStorageClient:
    """Supabase Storage backend (REST API via httpx)."""

    is_remote = True

    def __init__(self, url: str, key: str, timeout: float = _HTTP_TIMEOUT):
        self._base = f"{url.rstrip('/')}/storage/v1"
        self._timeout = timeout
        # One persistent client: connection pooling avoids repeated TLS
        # handshakes (and the transient timeouts they cause) on bulk uploads.
        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {key}",
                "apikey": key,
            },
            timeout=timeout,
        )
        # Exposed for scripts that need the same auth headers.
        self._headers = dict(self._client.headers)

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """HTTP request with a few retries on transient network errors."""
        last_exc: Exception | None = None
        for _ in range(_RETRIES):
            try:
                return self._client.request(method, url, **kwargs)
            except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout) as exc:
                last_exc = exc
        raise RuntimeError(
            f"Supabase Storage unreachable after {_RETRIES} tries: {last_exc}"
        )

    def upload(self, bucket: str, object_name: str, data: bytes) -> str:
        """Upload (upsert) *data* as *object_name* inside *bucket*."""
        name = sanitize_object_name(object_name)
        resp = self._request(
            "POST",
            f"{self._base}/object/{bucket}/{name}",
            headers={"Content-Type": "application/octet-stream", "x-upsert": "true"},
            content=data,
        )
        if resp.status_code not in (200, 201):
            raise RuntimeError(
                f"Supabase Storage upload failed ({resp.status_code}): {resp.text}"
            )
        return name

    def download(self, bucket: str, object_name: str) -> bytes:
        """Return object bytes. Raises FileNotFoundError if missing."""
        name = sanitize_object_name(object_name)
        resp = self._request("GET", f"{self._base}/object/{bucket}/{name}")
        if resp.status_code == 404:
            raise FileNotFoundError(f"No object '{name}' in bucket '{bucket}'.")
        if resp.status_code == 400 and (
            "NoSuchKey" in resp.text or "NoSuchBucket" in resp.text
        ):
            raise FileNotFoundError(f"No object '{name}' in bucket '{bucket}'.")
        if resp.status_code != 200:
            raise RuntimeError(
                f"Supabase Storage download failed ({resp.status_code}): {resp.text}"
            )
        return resp.content

    def delete(self, bucket: str, object_name: str) -> None:
        """Delete object. Missing objects are ignored (idempotent)."""
        name = sanitize_object_name(object_name)
        resp = self._request("DELETE", f"{self._base}/object/{bucket}/{name}")
        if resp.status_code not in (200, 204, 404):
            raise RuntimeError(
                f"Supabase Storage delete failed ({resp.status_code}): {resp.text}"
            )

    def exists(self, bucket: str, object_name: str) -> bool:
        try:
            self.download(bucket, object_name)
            return True
        except FileNotFoundError:
            return False


class LocalStorageClient:
    """Local-folder backend (development and tests only)."""

    is_remote = False

    def __init__(self, storage_dir: str, keys_dir: str):
        self._dirs = {
            BUCKET_ENCRYPTED: Path(storage_dir),
            BUCKET_KEYS: Path(keys_dir),
        }

    def _path(self, bucket: str, object_name: str) -> Path:
        directory = self._dirs[bucket]
        directory.mkdir(parents=True, exist_ok=True)
        return directory / sanitize_object_name(object_name)

    def upload(self, bucket: str, object_name: str, data: bytes) -> str:
        path = self._path(bucket, object_name)
        path.write_bytes(data)
        return path.name

    def download(self, bucket: str, object_name: str) -> bytes:
        path = self._path(bucket, object_name)
        if not path.exists():
            raise FileNotFoundError(f"No object '{path.name}' in {path.parent}.")
        return path.read_bytes()

    def delete(self, bucket: str, object_name: str) -> None:
        path = self._path(bucket, object_name)
        if path.exists():
            path.unlink()

    def exists(self, bucket: str, object_name: str) -> bool:
        return self._path(bucket, object_name).exists()


def get_storage():
    """Return the configured storage backend (Supabase in prod, else local)."""
    if USE_SUPABASE_STORAGE:
        return SupabaseStorageClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return LocalStorageClient(STORAGE_DIR, KEYS_DIR)
