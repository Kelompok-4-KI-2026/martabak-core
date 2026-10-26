import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from core.auth_security import decode_signed_token, get_current_user
from database import Base, engine, get_db, init_db
from models.user import User
from models.vault_file import VaultFile
from routers import auth_router, vault_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database schema is created and migrated
    init_db()
    yield


app = FastAPI(
    title="Martabak Core | Franchise Security Vault",
    description="Hyper-secure vault for culinary franchise assets, recipes, and PII.",
    version="1.0.0",
    lifespan=lifespan,
)

templates = Jinja2Templates(directory="templates")


def get_flashed_messages(with_categories: bool = False):
    return []


# Enable get_flashed_messages for Jinja2 templates
templates.env.globals["get_flashed_messages"] = get_flashed_messages

# Mount API routers
app.include_router(auth_router.router)
app.include_router(vault_router.router)


def get_optional_user(request: Request, db: Session) -> Optional[User]:
    token = request.cookies.get("session_token")
    if not token:
        auth_hdr = request.headers.get("authorization", "")
        if auth_hdr.startswith("Bearer "):
            token = auth_hdr.split(" ")[1].strip()

    if not token:
        return None

    user_id = decode_signed_token(token)
    if not user_id:
        return None

    return db.query(User).filter(User.id == user_id).first()


@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    files = (
        db.query(VaultFile)
        .filter(VaultFile.user_id == user.id)
        .order_by(VaultFile.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "files": files,
        },
    )


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if user:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": request.query_params.get("error"),
        },
    )


@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if user:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={
            "error": request.query_params.get("error"),
        },
    )


@app.get("/vault/{file_id}/inspect", response_class=HTMLResponse)
def inspect_page(file_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    file_record = (
        db.query(VaultFile)
        .filter(VaultFile.id == file_id, VaultFile.user_id == user.id)
        .first()
    )
    if not file_record:
        return RedirectResponse(url="/dashboard", status_code=303)

    if not os.path.exists(file_record.encrypted_filepath):
        return RedirectResponse(url="/dashboard", status_code=303)

    with open(file_record.encrypted_filepath, "rb") as f:
        ciphertext = f.read()

    try:
        from pathlib import Path
        from config import KEYS_DIR
        from core.key_manager import KeyManager
        key = KeyManager.load_key(file_record.key_id, keys_dir=Path(KEYS_DIR))
    except Exception:
        return RedirectResponse(url="/dashboard", status_code=303)

    from core.inspector import inspect_vault_payload
    report = inspect_vault_payload(file_record, ciphertext, key)

    return templates.TemplateResponse(
        request=request,
        name="inspect.html",
        context={
            "user": user,
            "report": report,
            "file": file_record,
        },
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Martabak Core Vault"}
