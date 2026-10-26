import io
import os
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from database import Base, engine, init_db
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    yield


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_render_login_page():
    response = client.get("/login")
    assert response.status_code == 200
    assert "Martabak Core" in response.text
    assert "Sign In" in response.text


def test_render_dashboard_unauthenticated_redirect():
    response = client.get("/dashboard", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_auth_workflow():
    # Register
    reg_payload = {
        "username": "franchisee_martabak_1",
        "email": "franchisee1@martabak.id",
        "password": "SuperSecretPassword123!"
    }
    res_reg = client.post("/api/v1/auth/register", json=reg_payload)
    assert res_reg.status_code in [200, 400]  # 400 if already created in rerun

    # Login
    login_data = {
        "email": "franchisee1@martabak.id",
        "password": "SuperSecretPassword123!"
    }
    res_login = client.post("/api/v1/auth/login", data=login_data)
    assert res_login.status_code == 200
    data = res_login.json()
    assert "access_token" in data
    token = data["access_token"]

    # Current user me
    res_me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    assert res_me.json()["username"] == "franchisee_martabak_1"


@pytest.mark.parametrize("cipher", ["AES", "DES", "RC4"])
def test_vault_upload_and_download_integrity(cipher):
    # Register user
    username = f"user_{cipher.lower()}"
    client.post("/api/v1/auth/register", json={
        "username": username,
        "email": f"{username}@martabak.id",
        "password": "SecretPassword123"
    })

    # Login
    login_res = client.post("/api/v1/auth/login", data={
        "username": username,
        "password": "SecretPassword123"
    })
    token = login_res.json()["access_token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    # Original secret file content (e.g. Secret recipe formula)
    original_content = f"RAHASIA RESEP MARTABAK MANIS BANGKA - CIPHER {cipher} - 2026".encode("utf-8") * 50
    fake_file = io.BytesIO(original_content)

    # Upload
    upload_res = client.post(
        "/api/v1/vault/upload",
        headers=auth_header,
        data={
            "file_type": "office_doc",
            "cipher_choice": cipher
        },
        files={
            "file": ("resep_rahasia.pdf", fake_file, "application/pdf")
        }
    )
    assert upload_res.status_code == 200
    upload_data = upload_res.json()
    assert upload_data["status"] == "success"
    file_id = upload_data["file_id"]
    assert upload_data["cipher_used"] == cipher

    # List files
    list_res = client.get("/api/v1/vault/files", headers=auth_header)
    assert list_res.status_code == 200
    user_files = list_res.json()
    assert any(f["id"] == file_id for f in user_files)

    # Download file and test binary integrity
    download_res = client.get(f"/api/v1/vault/download/{file_id}", headers=auth_header)
    assert download_res.status_code == 200
    assert download_res.content == original_content, f"Data integrity mismatch for {cipher}!"


def test_strict_user_isolation():
    # Create User A
    client.post("/api/v1/auth/register", json={
        "username": "user_a",
        "email": "user_a@martabak.id",
        "password": "PasswordA123"
    })
    token_a = client.post("/api/v1/auth/login", data={"username": "user_a", "password": "PasswordA123"}).json()["access_token"]

    # Create User B
    client.post("/api/v1/auth/register", json={
        "username": "user_b",
        "email": "user_b@martabak.id",
        "password": "PasswordB123"
    })
    token_b = client.post("/api/v1/auth/login", data={"username": "user_b", "password": "PasswordB123"}).json()["access_token"]

    # User A uploads a sensitive KTP scan
    fake_ktp = io.BytesIO(b"SENSITIVE_KTP_SCAN_USER_A")
    res_upload_a = client.post(
        "/api/v1/vault/upload",
        headers={"Authorization": f"Bearer {token_a}"},
        data={"file_type": "id_scan", "cipher_choice": "AES"},
        files={"file": ("ktp_user_a.png", fake_ktp, "image/png")}
    )
    file_id_a = res_upload_a.json()["file_id"]

    # User B attempts to access User A's file -> MUST BE 404 (Access Denied / Isolated)
    res_b_attempt = client.get(
        f"/api/v1/vault/download/{file_id_a}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert res_b_attempt.status_code == 404
    assert "File not found or access denied" in res_b_attempt.json()["detail"]

    # User B listing files must NOT include User A's file
    res_b_list = client.get("/api/v1/vault/files", headers={"Authorization": f"Bearer {token_b}"})
    assert res_b_list.status_code == 200
    assert all(f["id"] != file_id_a for f in res_b_list.json())


def test_signup_page_and_form_flow():
    # Clear session cookie to simulate unauthenticated visitor
    client.cookies.clear()

    # Test GET /signup renders page
    res_get = client.get("/signup")
    assert res_get.status_code == 200
    assert "Daftar Akun Baru" in res_get.text

    # Test POST /signup password mismatch
    res_mismatch = client.post(
        "/signup",
        data={
            "username": "outlet_baru",
            "email": "baru@martabak.id",
            "password": "Password123!",
            "confirm_password": "MismatchPassword!",
        },
        follow_redirects=False,
    )
    assert res_mismatch.status_code == 303
    assert "error=" in res_mismatch.headers["location"]

    # Test POST /signup successful
    res_success = client.post(
        "/signup",
        data={
            "username": "outlet_sukses",
            "email": "sukses@martabak.id",
            "password": "PasswordSukses123!",
            "confirm_password": "PasswordSukses123!",
            "full_name": "Pak Budi",
            "outlet_name": "Martabak Sukses",
        },
        follow_redirects=False,
    )
    assert res_success.status_code == 303
    assert res_success.headers["location"] == "/"
    assert "session_token" in res_success.cookies
