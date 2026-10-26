"""One-off migration: mirror martabak.db (SQLite) into the Supabase Postgres URL.

Reads every row from the local SQLite database and writes it to DATABASE_URL with
the original primary keys, so user_id foreign keys on vault_files stay valid.

Supabase currently holds rows created by the test suite (which has no DB isolation).
Those rows are cleared first, after being dumped to backups/ by the caller.

Usage:
    env -u PYTHONPATH .venv/bin/python scripts/migrate_sqlite_to_supabase.py [--dry-run]

Does not alter API routes or table structure.
"""

import argparse
import sqlite3
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config import DATABASE_URL  # noqa: E402

SQLITE_PATH = BASE_DIR / "martabak.db"

USER_COLS = [
    "id",
    "username",
    "email",
    "hashed_password",
    "full_name",
    "outlet_name",
    "created_at",
]
FILE_COLS = [
    "id",
    "user_id",
    "file_type",
    "original_filename",
    "encrypted_filepath",
    "cipher_used",
    "cipher_mode",
    "key_id",
    "iv_hex",
    "file_size",
    "created_at",
]


def read_sqlite():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    users = [dict(r) for r in conn.execute(
        f"SELECT {', '.join(USER_COLS)} FROM users ORDER BY id"
    )]
    files = [dict(r) for r in conn.execute(
        f"SELECT {', '.join(FILE_COLS)} FROM vault_files ORDER BY id"
    )]
    conn.close()
    return users, files


def insert_rows(conn, table, cols, rows):
    if not rows:
        return 0
    col_list = ", ".join(cols)
    params = ", ".join(f":{c}" for c in cols)
    stmt = text(f"INSERT INTO {table} ({col_list}) VALUES ({params})")
    for row in rows:
        conn.execute(stmt, {c: row[c] for c in cols})
    return len(rows)


def reset_sequence(conn, table, pk="id"):
    """Advance the Postgres sequence past MAX(id) so future inserts do not collide."""
    conn.execute(text(
        f"SELECT setval(pg_get_serial_sequence('{table}', '{pk}'), "
        f"(SELECT COALESCE(MAX({pk}), 0) FROM {table}), true)"
    ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if DATABASE_URL.startswith("sqlite"):
        sys.exit("DATABASE_URL still points at SQLite - aborting.")

    users, files = read_sqlite()
    print(f"source (martabak.db): {len(users)} users, {len(files)} vault_files")

    engine = create_engine(DATABASE_URL)
    with engine.begin() as conn:
        existing_users = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
        existing_files = conn.execute(text("SELECT COUNT(*) FROM vault_files")).scalar()
        print(f"target (supabase) before: {existing_users} users, {existing_files} vault_files")

        if args.dry_run:
            print("dry-run: no changes written.")
            return

        # Clear test-suite artifacts. vault_files first (FK -> users.id).
        conn.execute(text("DELETE FROM vault_files"))
        conn.execute(text("DELETE FROM users"))

        n_users = insert_rows(conn, "users", USER_COLS, users)
        n_files = insert_rows(conn, "vault_files", FILE_COLS, files)

        reset_sequence(conn, "users")
        reset_sequence(conn, "vault_files")

    with engine.connect() as conn:
        after_users = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
        after_files = conn.execute(text("SELECT COUNT(*) FROM vault_files")).scalar()
        print(f"target (supabase) after:  {after_users} users, {after_files} vault_files")
        print(f"inserted: {n_users} users, {n_files} vault_files")

    assert after_users == len(users), "user count mismatch"
    assert after_files == len(files), "vault_files count mismatch"
    print("OK: supabase now mirrors martabak.db")


if __name__ == "__main__":
    main()
