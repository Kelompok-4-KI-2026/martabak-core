import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from core.auth_security import decode_signed_token, get_current_user
from database import Base, engine, get_db
from models.user import User
from models.vault_file import VaultFile
from routers import auth_router, vault_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database schema is created
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Martabak Core | Franchise Security Vault",
    description="Hyper-secure vault for culinary franchise assets, recipes, and PII.",
    version="1.0.0",
    lifespan=lifespan,
)

templates = Jinja2Templates(directory="templates")

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
        "dashboard.html",
        {
            "request": request,
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
        "login.html",
        {
            "request": request,
            "error": request.query_params.get("error"),
        },
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Martabak Core Vault"}
