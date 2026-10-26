#!/usr/bin/env python3
"""
Script verifikasi koneksi database (SQLite / Supabase PostgreSQL)
Menjalankan migrasi skema tabel secara otomatis.
"""
import sys
from config import DATABASE_URL
from database import engine, Base
from models.user import User
from models.vault_file import VaultFile

def main():
    masked_url = DATABASE_URL
    if "@" in masked_url:
        prefix, host = masked_url.split("@", 1)
        proto = prefix.split("://")[0]
        masked_url = f"{proto}://*****:*****@{host}"
    
    print("=" * 60)
    print("MARTABAK CORE - DATABASE CONNECTION TEST")
    print("=" * 60)
    print(f"Target Database URL: {masked_url}")
    print("Mencoba menghubungkan ke database...")

    try:
        # Coba konek & buat tabel
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            print("Status: BERHASIL TERHUBUNG!")
            print("Semua tabel (users, vault_files) berhasil dibuat / diverifikasi.")
            print("=" * 60)
            sys.exit(0)
    except Exception as e:
        print("Status: GAGAL KONEKSI!")
        print(f"Error detail: {e}")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
