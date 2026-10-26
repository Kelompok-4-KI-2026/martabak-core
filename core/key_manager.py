"""
core/key_manager.py
===================
Secure key persistence layer for Martabak Core.

Design
------
* Each encryption key is stored as a **separate binary file** under a
  ``keys/`` directory that sits outside the source tree.
* File permissions are locked to **0o600** (owner read/write only)
  immediately after creation.
* Key material never enters the database — the database stores only the
  UUID identifier, which the backend uses to call load_key() at decrypt time.

Usage (by the backend / Person 2)
----------------------------------
    from core.key_manager import KeyManager

    # After encrypting a file:
    key_id = str(uuid.uuid4())
    KeyManager.save_key(result["key"], key_id)

    # When decrypting:
    key = KeyManager.load_key(key_id)
"""

import os
import stat
from pathlib import Path

# Default storage directory (relative to the project root).
# The backend can override this by passing a custom `keys_dir` argument.
_DEFAULT_KEYS_DIR = Path(__file__).resolve().parent.parent / "keys"


class KeyManager:
    """
    Utility class for persisting and retrieving encryption keys.

    All methods accept an optional *keys_dir* parameter so the storage
    location can be overridden in tests or different deployment environments.
    """

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_dir(keys_dir: Path | None) -> Path:
        """Return the keys directory, creating it (mode 0o700) if needed."""
        directory = Path(keys_dir) if keys_dir else _DEFAULT_KEYS_DIR
        directory.mkdir(parents=True, exist_ok=True)
        # Restrict directory access to owner only
        os.chmod(directory, stat.S_IRWXU)
        return directory

    @staticmethod
    def _key_path(identifier: str, directory: Path) -> Path:
        """Build the full path for a key file given its identifier."""
        # Sanitise the identifier to prevent path-traversal attacks
        safe_id = Path(identifier).name
        return directory / f"{safe_id}.key"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @staticmethod
    def save_key(
        key: bytes,
        identifier: str,
        keys_dir: Path | None = None,
    ) -> Path:
        """
        Persist *key* bytes to disk under ``keys/<identifier>.key``.

        Parameters
        ----------
        key : bytes
            Raw key bytes returned by :meth:`MartabakCipherEngine.encrypt_data`.
        identifier : str
            A unique string (e.g., a UUID) that the backend stores in the DB
            and uses later to retrieve the key.
        keys_dir : Path | None
            Override the storage directory (defaults to ``keys/`` in the
            project root).

        Returns
        -------
        Path
            Absolute path of the written key file.

        Raises
        ------
        ValueError
            If *identifier* is empty or contains path-separators.
        """
        if not identifier or identifier != Path(identifier).name:
            raise ValueError(
                f"Invalid key identifier: '{identifier}'. "
                "Must be a plain filename with no path separators."
            )

        directory = KeyManager._resolve_dir(keys_dir)
        path = KeyManager._key_path(identifier, directory)

        path.write_bytes(key)
        # Restrict the key file to owner read/write only
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

        return path

    @staticmethod
    def load_key(
        identifier: str,
        keys_dir: Path | None = None,
    ) -> bytes:
        """
        Retrieve the key bytes for *identifier*.

        Parameters
        ----------
        identifier : str
            The same identifier that was passed to :meth:`save_key`.
        keys_dir : Path | None
            Override the storage directory.

        Returns
        -------
        bytes
            The raw key bytes.

        Raises
        ------
        FileNotFoundError
            If no key file exists for *identifier*.
        """
        directory = KeyManager._resolve_dir(keys_dir)
        path = KeyManager._key_path(identifier, directory)

        if not path.exists():
            raise FileNotFoundError(
                f"No key found for identifier '{identifier}' in {directory}."
            )

        return path.read_bytes()

    @staticmethod
    def delete_key(
        identifier: str,
        keys_dir: Path | None = None,
    ) -> None:
        """
        Permanently remove the key file for *identifier*.

        Call this after a file has been decrypted and delivered to the user,
        or when a file record is deleted from the system.

        Parameters
        ----------
        identifier : str
            The identifier whose key should be deleted.
        keys_dir : Path | None
            Override the storage directory.

        Raises
        ------
        FileNotFoundError
            If the key file does not exist.
        """
        directory = KeyManager._resolve_dir(keys_dir)
        path = KeyManager._key_path(identifier, directory)

        if not path.exists():
            raise FileNotFoundError(
                f"Cannot delete: no key found for identifier '{identifier}'."
            )

        path.unlink()

    @staticmethod
    def key_exists(
        identifier: str,
        keys_dir: Path | None = None,
    ) -> bool:
        """
        Return ``True`` if a key file exists for *identifier*, else ``False``.

        Useful for backend validation before attempting decryption.

        Parameters
        ----------
        identifier : str
            The identifier to check.
        keys_dir : Path | None
            Override the storage directory.
        """
        directory = KeyManager._resolve_dir(keys_dir)
        path = KeyManager._key_path(identifier, directory)
        return path.exists()
