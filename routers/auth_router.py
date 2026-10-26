from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from core.auth_security import (
    create_signed_token,
    get_current_user,
    hash_password,
    verify_password,
)
from database import get_db
from models.user import User
from schemas.auth_schema import UserOut, UserRegister

router = APIRouter(tags=["Authentication"])


@router.post("/api/v1/auth/register", response_model=UserOut)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == user_in.username) |
        (User.email == user_in.email if user_in.email else False)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
        outlet_name=user_in.outlet_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/signup")
def signup_form(
    response: Response,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    full_name: Optional[str] = Form(None),
    outlet_name: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    from urllib.parse import quote

    username = username.strip()
    email = email.strip()
    if not username or not email or not password:
        return RedirectResponse(
            url="/signup?error=" + quote("Semua field wajib diisi."),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    if len(password) < 8:
        return RedirectResponse(
            url="/signup?error=" + quote("Passphrase minimal 8 karakter."),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    if password != confirm_password:
        return RedirectResponse(
            url="/signup?error=" + quote("Konfirmasi passphrase tidak cocok."),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    existing = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing:
        return RedirectResponse(
            url="/signup?error=" + quote("Username atau email sudah terdaftar."),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name.strip() if full_name else None,
        outlet_name=outlet_name.strip() if outlet_name else None,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_signed_token(new_user.id)
    redirect = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    redirect.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax",
    )
    return redirect


@router.post("/api/v1/auth/login")
def login_api(
    response: Response,
    email: Optional[str] = Form(None),
    username: Optional[str] = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    login_id = email or username
    if not login_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username is required"
        )

    user = db.query(User).filter(
        (User.email == login_id) | (User.username == login_id)
    ).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_signed_token(user.id)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax",
    )
    return {
        "status": "success",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    }


@router.post("/login")
def login_form(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        (User.email == email) | (User.username == email)
    ).first()

    if not user or not verify_password(password, user.hashed_password):
        return RedirectResponse(
            url="/login?error=Invalid+credentials",
            status_code=status.HTTP_303_SEE_OTHER
        )

    token = create_signed_token(user.id)
    redirect = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    redirect.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax",
    )
    return redirect


@router.get("/logout")
@router.post("/api/v1/auth/logout")
def logout(response: Response):
    redirect = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    redirect.delete_cookie(key="session_token")
    return redirect


@router.get("/api/v1/auth/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
