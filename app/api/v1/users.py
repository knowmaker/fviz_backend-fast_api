# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.user import (
    RegisterRequest,
    ConfirmRequest,
    LoginRequest,
    TokenResponse,
    UserRead,
    UserUpdate,
)
from app.services.user_service import register_user, confirm_user, login_user, update_user_profile

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(db, email=payload.email, password=payload.password)
        return {
            "message": "User created (or already exists and not confirmed). Confirmation code was sent.",
            "email": user.email,
            "is_confirmed": user.is_confirmed,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/confirm")
def confirm(payload: ConfirmRequest, db: Session = Depends(get_db)):
    ok = confirm_user(db, email=payload.email, code=payload.code)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or confirmation code",
        )
    return {"message": "User confirmed"}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, email=payload.email, password=payload.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or user not confirmed",
        )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserRead)
def update_me(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_user_profile(db, user=current_user, data=payload)
