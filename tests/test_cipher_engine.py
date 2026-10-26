"""
tests/test_cipher_engine.py
===========================
Unit tests for MartabakCipherEngine and KeyManager.

Acceptance criteria covered (from PRD_PERSON_1_CRYPTO.md)
----------------------------------------------------------
[x] Code runs without padding or key-size errors.
[x] AES, DES, RC4 each produce 100 % identical plaintext on decryption.
[x] Unsupported cipher raises ValueError.
[x] KeyManager save / load / delete / key_exists round-trip.
[x] Path-traversal attack on key identifier is rejected.
"""

import tempfile
from pathlib import Path

import pytest

from core.cipher_engine import MartabakCipherEngine
from core.key_manager import KeyManager

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

# A representative plaintext payload — mix of text and binary-ish bytes so we
# exercise both padding (block ciphers) and stream mode (RC4) realistically.
SAMPLE_TEXT = b"Martabak Core crypto test payload - 2026"
SAMPLE_BINARY = bytes(range(256)) * 4   # 1 KiB of every byte value


# ---------------------------------------------------------------------------
# MartabakCipherEngine — encrypt / decrypt round-trip tests
# ---------------------------------------------------------------------------

class TestAES:
    """AES-256-CBC round-trip and integrity."""

    def test_roundtrip_text(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "AES")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "AES", iv=result["iv"]
        )
        assert recovered == SAMPLE_TEXT

    def test_roundtrip_binary(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_BINARY, "AES")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "AES", iv=result["iv"]
        )
        assert recovered == SAMPLE_BINARY

    def test_integrity_helper(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "AES")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "AES", iv=result["iv"]
        )
        assert MartabakCipherEngine.verify_integrity(SAMPLE_TEXT, recovered)

    def test_case_insensitive_input(self):
        """cipher_type should accept lowercase too."""
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "aes")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "aes", iv=result["iv"]
        )
        assert recovered == SAMPLE_TEXT

    def test_metadata_fields(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "AES")
        assert result["mode"] == "CBC"
        assert result["cipher_type"] == "AES"
        assert result["iv"] is not None
        assert len(result["key"]) == 32   # 256-bit

    def test_fresh_iv_each_call(self):
        """Two separate encryptions of the same plaintext must produce different IVs."""
        r1 = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "AES")
        r2 = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "AES")
        assert r1["iv"] != r2["iv"]

    def test_missing_iv_raises(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "AES")
        with pytest.raises(ValueError, match="IV is required"):
            MartabakCipherEngine.decrypt_data(
                result["ciphertext"], result["key"], "AES", iv=None
            )


class TestDES:
    """DES-CBC round-trip and integrity."""

    def test_roundtrip_text(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "DES")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "DES", iv=result["iv"]
        )
        assert recovered == SAMPLE_TEXT

    def test_roundtrip_binary(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_BINARY, "DES")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "DES", iv=result["iv"]
        )
        assert recovered == SAMPLE_BINARY

    def test_integrity_helper(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "DES")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "DES", iv=result["iv"]
        )
        assert MartabakCipherEngine.verify_integrity(SAMPLE_TEXT, recovered)

    def test_metadata_fields(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "DES")
        assert result["mode"] == "CBC"
        assert result["cipher_type"] == "DES"
        assert result["iv"] is not None
        assert len(result["key"]) == 8    # 64-bit

    def test_missing_iv_raises(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "DES")
        with pytest.raises(ValueError, match="IV is required"):
            MartabakCipherEngine.decrypt_data(
                result["ciphertext"], result["key"], "DES", iv=None
            )


class TestRC4:
    """RC4 stream cipher round-trip and integrity."""

    def test_roundtrip_text(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "RC4")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "RC4"
        )
        assert recovered == SAMPLE_TEXT

    def test_roundtrip_binary(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_BINARY, "RC4")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "RC4"
        )
        assert recovered == SAMPLE_BINARY

    def test_integrity_helper(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "RC4")
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], result["key"], "RC4"
        )
        assert MartabakCipherEngine.verify_integrity(SAMPLE_TEXT, recovered)

    def test_metadata_fields(self):
        result = MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, "RC4")
        assert result["mode"] == "STREAM"
        assert result["cipher_type"] == "RC4"
        assert result["iv"] is None        # Stream cipher — no IV
        assert len(result["key"]) == 16   # 128-bit


class TestUnsupportedCipher:
    """Invalid cipher_type must always raise ValueError."""

    @pytest.mark.parametrize("bad_cipher", ["ECB", "3DES", "RSA", "", "blowfish"])
    def test_encrypt_raises(self, bad_cipher):
        with pytest.raises(ValueError):
            MartabakCipherEngine.encrypt_data(SAMPLE_TEXT, bad_cipher)

    @pytest.mark.parametrize("bad_cipher", ["ECB", "3DES", "RSA", "", "blowfish"])
    def test_decrypt_raises(self, bad_cipher):
        with pytest.raises(ValueError):
            MartabakCipherEngine.decrypt_data(b"dummy", b"key", bad_cipher)


# ---------------------------------------------------------------------------
# KeyManager — persistence round-trip tests
# ---------------------------------------------------------------------------

class TestKeyManager:
    """KeyManager save / load / delete / key_exists tests."""

    @pytest.fixture()
    def tmp_keys_dir(self, tmp_path):
        """Provide a clean temporary directory for each test."""
        return tmp_path / "keys"

    def test_save_and_load(self, tmp_keys_dir):
        key = b"\xde\xad\xbe\xef" * 8   # 32 bytes
        KeyManager.save_key(key, "test-id-1", keys_dir=tmp_keys_dir)
        assert KeyManager.load_key("test-id-1", keys_dir=tmp_keys_dir) == key

    def test_key_exists_true(self, tmp_keys_dir):
        KeyManager.save_key(b"somekey1", "exists-id", keys_dir=tmp_keys_dir)
        assert KeyManager.key_exists("exists-id", keys_dir=tmp_keys_dir) is True

    def test_key_exists_false(self, tmp_keys_dir):
        assert KeyManager.key_exists("ghost-id", keys_dir=tmp_keys_dir) is False

    def test_delete_key(self, tmp_keys_dir):
        KeyManager.save_key(b"todelete!", "del-id", keys_dir=tmp_keys_dir)
        KeyManager.delete_key("del-id", keys_dir=tmp_keys_dir)
        assert KeyManager.key_exists("del-id", keys_dir=tmp_keys_dir) is False

    def test_load_missing_raises(self, tmp_keys_dir):
        with pytest.raises(FileNotFoundError):
            KeyManager.load_key("no-such-id", keys_dir=tmp_keys_dir)

    def test_delete_missing_raises(self, tmp_keys_dir):
        with pytest.raises(FileNotFoundError):
            KeyManager.delete_key("no-such-id", keys_dir=tmp_keys_dir)

    def test_path_traversal_rejected(self, tmp_keys_dir):
        with pytest.raises(ValueError):
            KeyManager.save_key(b"hack", "../../../etc/passwd", keys_dir=tmp_keys_dir)

    def test_file_permissions(self, tmp_keys_dir):
        """Key file must be readable only by the owner (0o600)."""
        key = b"secret_key_bytes"
        path = KeyManager.save_key(key, "perm-test-id", keys_dir=tmp_keys_dir)
        mode = oct(path.stat().st_mode & 0o777)
        assert mode == "0o600", f"Expected 0o600, got {mode}"

    def test_roundtrip_with_cipher_engine(self, tmp_keys_dir):
        """Full end-to-end: encrypt → save key → load key → decrypt."""
        payload = b"Top secret franchise document contents."
        result = MartabakCipherEngine.encrypt_data(payload, "AES")

        key_id = "franchise-doc-uuid-001"
        KeyManager.save_key(result["key"], key_id, keys_dir=tmp_keys_dir)

        loaded_key = KeyManager.load_key(key_id, keys_dir=tmp_keys_dir)
        recovered = MartabakCipherEngine.decrypt_data(
            result["ciphertext"], loaded_key, "AES", iv=result["iv"]
        )

        assert recovered == payload
        assert MartabakCipherEngine.verify_integrity(payload, recovered)
