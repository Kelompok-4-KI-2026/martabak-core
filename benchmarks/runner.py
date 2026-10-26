import json
from pathlib import Path
import platform
import statistics
import sys
import time
import tracemalloc

from core.cipher_engine import MartabakCipherEngine


def run_benchmarks():
  output_path = Path(__file__).resolve().parent / "report_data.json"

  test_payloads = {
      "Small PII Data (1 KB)": b"A" * 1024,
      "Medium Office Doc (500 KB)": b"B" * (500 * 1024),
      "Heavy SOP Video (5 MB)": b"C" * (5 * 1024 * 1024),
  }

  ciphers = ["AES", "DES", "RC4"]
  iterations = 5

  # 1. Warm-up run untuk menghilangkan cold-start overhead
  dummy_data = b"Warmup" * 100
  for c in ciphers:
    enc_w = MartabakCipherEngine.encrypt_data(dummy_data, c)
    MartabakCipherEngine.decrypt_data(
        enc_w["ciphertext"], enc_w["key"], c, enc_w.get("iv")
    )

  benchmark_data = {
      "environment": {
          "python_version": sys.version.split()[0],
          "platform": platform.platform(),
          "processor": platform.processor() or "Unknown Processor",
          "iterations": iterations,
          "timer": "time.perf_counter",
      },
      "results": {},
  }

  # 2. Pengujian Utama & Profiling Memori
  for label, data in test_payloads.items():
    benchmark_data["results"][label] = {}
    size_mib = len(data) / (1024**2)

    for cipher in ciphers:
      enc_times = []
      dec_times = []

      # Mulai lacak alokasi memori
      tracemalloc.start()

      for _ in range(iterations):
        # Ukur durasi Enkripsi
        t0 = time.perf_counter()
        encrypted = MartabakCipherEngine.encrypt_data(data, cipher)
        enc_times.append((time.perf_counter() - t0) * 1000)

        # Ukur durasi Dekripsi & Verifikasi Integritas Data Utuh
        t0 = time.perf_counter()
        decrypted = MartabakCipherEngine.decrypt_data(
            encrypted["ciphertext"],
            encrypted["key"],
            cipher,
            encrypted.get("iv"),
        )
        dec_times.append((time.perf_counter() - t0) * 1000)

        if decrypted != data:
          raise ValueError(
              f"Integrity check GAGAL untuk {label} menggunakan {cipher}!"
          )

      _, peak_bytes = tracemalloc.get_traced_memory()
      tracemalloc.stop()

      median_enc_ms = statistics.median(enc_times)
      median_dec_ms = statistics.median(dec_times)

      enc_throughput = (
          size_mib / (median_enc_ms / 1000) if median_enc_ms > 0 else 0
      )
      dec_throughput = (
          size_mib / (median_dec_ms / 1000) if median_dec_ms > 0 else 0
      )

      benchmark_data["results"][label][cipher] = {
          "median_encryption_ms": round(median_enc_ms, 3),
          "median_decryption_ms": round(median_dec_ms, 3),
          "encryption_throughput_mib_s": round(enc_throughput, 2),
          "decryption_throughput_mib_s": round(dec_throughput, 2),
          "peak_memory_kib": round(peak_bytes / 1024, 2),
          "integrity_ok": True,
          "raw_encryption_runs_ms": [round(x, 3) for x in enc_times],
          "raw_decryption_runs_ms": [round(x, 3) for x in dec_times],
      }

      print(
          f"[{label}] {cipher} -> Enc: {median_enc_ms:.2f}ms"
          f" ({enc_throughput:.1f} MiB/s) | Dec: {median_dec_ms:.2f}ms | Mem:"
          f" {peak_bytes / 1024:.1f} KiB | Integrity: OK"
      )

  # Simpan hasil analisis ke report_data.json
  with output_path.open("w", encoding="utf-8") as f:
    json.dump(benchmark_data, f, indent=4)

  print(
      f"\nBenchmark final selesai! Data akurat tersimpan di: {output_path.name}"
  )


if __name__ == "__main__":
  run_benchmarks()