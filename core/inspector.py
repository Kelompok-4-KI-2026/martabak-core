"""
core/inspector.py
=================
Cryptographic analysis and inspection utilities for Martabak Core Vault:
- Shannon Entropy calculation
- Hex dump formatter with ASCII alignment
- Block architecture mapping (AES-CBC, DES-CBC, RC4 Stream)
- Avalanche Effect (efek longsoran) demonstration with bit-level diffusion analysis
"""

import math
import os
from collections import Counter
from typing import Any, Dict, List
from Crypto.Cipher import AES, ARC4, DES


def calculate_entropy(data: bytes) -> Dict[str, Any]:
    """
    Calculate Shannon entropy of the given byte sequence:
    H = - sum( p(x) * log2(p(x)) )
    Range: 0.0 (uniform/zero information) to 8.0 (ideal cryptographically random).
    """
    if not data:
        return {
            "value": 0.0,
            "max": 8.0,
            "percentage": 0.0,
            "rating": "Kosong",
            "description": "Tidak ada data payload yang diinspeksi.",
        }

    total = len(data)
    counts = Counter(data)
    entropy = -sum((cnt / total) * math.log2(cnt / total) for cnt in counts.values())
    entropy = round(entropy, 4)
    pct = round((entropy / 8.0) * 100, 2)

    if entropy >= 7.8:
        rating = "Tinggi (Kriptografis Acak)"
        desc = "Distribusi byte seragam menyerupai white noise. Tidak ada pola statistik plaintext yang bocor."
    elif entropy >= 6.5:
        rating = "Sedang"
        desc = "Terdapat sedikit variasi statistik, umum pada payload berukuran sangat kecil dengan padding."
    else:
        rating = "Rendah"
        desc = "Entropi rendah menunjukkan pola data terstruktur atau redundansi tinggi."

    return {
        "value": entropy,
        "max": 8.0,
        "percentage": pct,
        "rating": rating,
        "description": desc,
    }


def generate_hex_dump(data: bytes, max_bytes: int = 256) -> List[Dict[str, Any]]:
    """
    Generate an aligned hex dump with 16 bytes per line:
    - offset: 8 hex chars (e.g. 00000000)
    - hex_bytes: list of 2-char hex strings
    - ascii: printable ASCII or '.'
    """
    slice_data = data[:max_bytes]
    rows = []
    for i in range(0, len(slice_data), 16):
        chunk = slice_data[i:i + 16]
        hex_bytes = [f"{b:02X}" for b in chunk]
        ascii_chars = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        rows.append({
            "offset": f"{i:08X}",
            "hex_bytes": hex_bytes,
            "ascii": ascii_chars,
        })
    return rows


def generate_block_map(cipher_used: str, ciphertext_len: int) -> Dict[str, Any]:
    """
    Map ciphertext structure into cryptographic blocks or stream units.
    """
    cipher_upper = cipher_used.upper()
    if cipher_upper == "AES":
        block_size = 16
        mode = "CBC (Chaining Block)"
    elif cipher_upper == "DES":
        block_size = 8
        mode = "CBC (Chaining Block)"
    else:  # RC4
        block_size = 1
        mode = "STREAM (Keystream XOR)"

    block_count = (ciphertext_len // block_size) if block_size > 0 else ciphertext_len
    return {
        "block_size_bytes": block_size,
        "block_size_bits": block_size * 8,
        "block_count": block_count,
        "mode": mode,
        "ciphertext_total_bytes": ciphertext_len,
    }


def compute_avalanche_demo(cipher_used: str, key: bytes) -> Dict[str, Any]:
    """
    Demonstrate the Avalanche Effect (efek longsoran):
    Flip exactly 1 bit in a test plaintext, encrypt both with identical key & IV,
    and measure the Hamming distance (bit differences) in ciphertext.
    - AES & DES (block ciphers): ideal avalanche ~50% bit diffusion across block
    - RC4 (stream cipher): flips exactly 1 bit (0.78% on 16B), illustrating lack of diffusion
    """
    cipher_upper = cipher_used.upper()
    block_size = 8 if cipher_upper == "DES" else 16

    # Original sample plaintext
    p1 = os.urandom(block_size)
    # Flipped plaintext: exactly 1 bit toggled in first byte
    p2_arr = bytearray(p1)
    p2_arr[0] ^= 0x01
    p2 = bytes(p2_arr)

    # Identical IV to isolate the cipher core's internal diffusion
    iv = os.urandom(block_size) if cipher_upper in ["AES", "DES"] else None

    if cipher_upper == "AES":
        c1 = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(p1)
        c2 = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(p2)
    elif cipher_upper == "DES":
        c1 = DES.new(key, DES.MODE_CBC, iv=iv).encrypt(p1)
        c2 = DES.new(key, DES.MODE_CBC, iv=iv).encrypt(p2)
    else:  # RC4
        c1 = ARC4.new(key).encrypt(p1)
        c2 = ARC4.new(key).encrypt(p2)

    total_bits = len(c1) * 8
    bit_diff_count = sum(bin(b1 ^ b2).count("1") for b1, b2 in zip(c1, c2))
    bit_diff_pct = round((bit_diff_count / total_bits) * 100, 2)

    if cipher_upper == "RC4":
        analysis = "Stream cipher tidak memiliki difusi blok: pembalikan 1 bit pada plaintext menghasilkan tepat 1 bit perubahan pada ciphertext."
        rating = "Khas Stream Cipher (1 bit)"
    elif 40.0 <= bit_diff_pct <= 60.0:
        analysis = "Efek longsoran mendekati nilai ideal 50%. Satu bit perubahan input menyebar acak ke seluruh blok sandi."
        rating = "Sangat Baik (Difusi Ideal)"
    else:
        analysis = f"Terdeteksi difusi sebesar {bit_diff_pct}%, membuktikan keteracakan blok cipher."
        rating = "Aktif (Difusi Kuat)"

    return {
        "p1_hex": p1.hex().upper(),
        "p2_hex": p2.hex().upper(),
        "c1_hex": c1.hex().upper(),
        "c2_hex": c2.hex().upper(),
        "bit_diff_count": bit_diff_count,
        "total_bits": total_bits,
        "bit_diff_pct": bit_diff_pct,
        "rating": rating,
        "analysis": analysis,
    }


def inspect_vault_payload(
    file_record: Any,
    ciphertext: bytes,
    key: bytes,
) -> Dict[str, Any]:
    """
    Generate comprehensive cryptographic inspection report for a vault item.
    """
    entropy_info = calculate_entropy(ciphertext)
    hex_rows = generate_hex_dump(ciphertext, max_bytes=256)
    block_info = generate_block_map(file_record.cipher_used, len(ciphertext))
    avalanche_info = compute_avalanche_demo(file_record.cipher_used, key)

    return {
        "file_id": file_record.id,
        "original_filename": file_record.original_filename,
        "file_type": file_record.file_type,
        "cipher_used": file_record.cipher_used,
        "cipher_mode": file_record.cipher_mode,
        "original_size": file_record.file_size,
        "ciphertext_size": len(ciphertext),
        "iv_hex": file_record.iv_hex,
        "key_id": file_record.key_id,
        "entropy": entropy_info,
        "hex_preview": hex_rows,
        "hex_preview_bytes": min(len(ciphertext), 256),
        "block_map": block_info,
        "avalanche": avalanche_info,
    }
