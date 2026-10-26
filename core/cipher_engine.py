"""
core/cipher_engine.py
=====================
Cryptographic engine for Martabak Core.

Supported ciphers
-----------------
* AES-256-CBC  (pycryptodome AES + PKCS7 padding)
* DES-CBC      (pycryptodome DES + PKCS7 padding)
* RC4          (pycryptodome ARC4 stream cipher)

Rules enforced
--------------
* ECB mode is NEVER used (assignment constraint).
* Every encrypt call generates a fresh random key + IV via os.urandom().
* decrypt_data returns the original bytes 100 % intact (PKCS7 unpad for
  block ciphers; direct XOR-stream inversion for RC4).
"""

import os

from Crypto.Cipher import AES, ARC4, DES
from Crypto.Util.Padding import pad, unpad


class MartabakCipherEngine:
    """
    Core encryption / decryption engine supporting AES, DES, and RC4.

    All block-cipher operations use CBC mode with a randomly generated IV.
    RC4 is a stream cipher and therefore requires no IV.

    Both encrypt_data and decrypt_data work on raw *bytes* so they are
    completely file-format-agnostic (PDFs, images, videos, etc.).
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @staticmethod
    def encrypt_data(file_bytes: bytes, cipher_type: str) -> dict:
        """
        Encrypt *file_bytes* with the requested cipher.

        Parameters
        ----------
        file_bytes : bytes
            Raw binary content of the file to encrypt.
        cipher_type : str
            One of ``"AES"``, ``"DES"``, or ``"RC4"`` (case-insensitive).

        Returns
        -------
        dict with keys:
            ``ciphertext`` (bytes)  – encrypted payload
            ``key``        (bytes)  – randomly generated secret key
            ``iv``         (bytes | None) – initialisation vector (None for RC4)
            ``mode``       (str)    – ``"CBC"`` or ``"STREAM"``
            ``cipher_type``(str)    – normalised cipher name (upper-case)

        Raises
        ------
        ValueError
            If *cipher_type* is not one of the supported values.
        """
        cipher_type = cipher_type.upper()

        if cipher_type == "AES":
            key = os.urandom(32)                          # 256-bit key
            cipher = AES.new(key, AES.MODE_CBC)           # fresh random IV
            ciphertext = cipher.encrypt(pad(file_bytes, AES.block_size))
            return {
                "ciphertext": ciphertext,
                "key": key,
                "iv": cipher.iv,
                "mode": "CBC",
                "cipher_type": "AES",
            }

        elif cipher_type == "DES":
            key = os.urandom(8)                           # 64-bit key (DES requirement)
            cipher = DES.new(key, DES.MODE_CBC)           # fresh random IV
            ciphertext = cipher.encrypt(pad(file_bytes, DES.block_size))
            return {
                "ciphertext": ciphertext,
                "key": key,
                "iv": cipher.iv,
                "mode": "CBC",
                "cipher_type": "DES",
            }

        elif cipher_type == "RC4":
            key = os.urandom(16)                          # 128-bit key
            cipher = ARC4.new(key)
            ciphertext = cipher.encrypt(file_bytes)
            return {
                "ciphertext": ciphertext,
                "key": key,
                "iv": None,                               # stream cipher – no IV
                "mode": "STREAM",
                "cipher_type": "RC4",
            }

        else:
            raise ValueError(
                f"Unsupported cipher type: '{cipher_type}'. "
                "Choose one of: AES, DES, RC4."
            )

    @staticmethod
    def decrypt_data(
        ciphertext: bytes,
        key: bytes,
        cipher_type: str,
        iv: bytes | None = None,
    ) -> bytes:
        """
        Decrypt *ciphertext* back to the original raw bytes.

        Parameters
        ----------
        ciphertext : bytes
            The encrypted payload returned by :meth:`encrypt_data`.
        key : bytes
            The secret key returned by :meth:`encrypt_data`.
        cipher_type : str
            One of ``"AES"``, ``"DES"``, or ``"RC4"`` (case-insensitive).
        iv : bytes | None
            Initialisation vector (required for AES/DES, ``None`` for RC4).

        Returns
        -------
        bytes
            Original file bytes – guaranteed to be an exact binary match
            with the input passed to :meth:`encrypt_data`.

        Raises
        ------
        ValueError
            If *cipher_type* is unsupported, or if *iv* is missing for a
            block cipher.
        """
        cipher_type = cipher_type.upper()

        if cipher_type == "AES":
            if iv is None:
                raise ValueError("IV is required for AES-CBC decryption.")
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            return unpad(cipher.decrypt(ciphertext), AES.block_size)

        elif cipher_type == "DES":
            if iv is None:
                raise ValueError("IV is required for DES-CBC decryption.")
            cipher = DES.new(key, DES.MODE_CBC, iv=iv)
            return unpad(cipher.decrypt(ciphertext), DES.block_size)

        elif cipher_type == "RC4":
            cipher = ARC4.new(key)
            return cipher.decrypt(ciphertext)

        else:
            raise ValueError(
                f"Unsupported cipher type: '{cipher_type}'. "
                "Choose one of: AES, DES, RC4."
            )

    @staticmethod
    def verify_integrity(original: bytes, decrypted: bytes) -> bool:
        """
        Confirm that decryption produced an exact binary match.

        Parameters
        ----------
        original : bytes
            The plaintext that was originally encrypted.
        decrypted : bytes
            The result of :meth:`decrypt_data`.

        Returns
        -------
        bool
            ``True`` if the bytes are identical, ``False`` otherwise.
        """
        return original == decrypted
