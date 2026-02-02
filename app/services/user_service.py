# app/services/user_service.py
import secrets
import string
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.schemas.user import UserUpdate


def _norm_email(email: str) -> str:
    return email.strip().lower()


def _generate_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def register_user(db: Session, email: str) -> User:
    email_norm = _norm_email(email)
    existing = db.query(User).filter(User.email == email_norm).first()
    if existing:
        raise ValueError("User already registered")

    plain_password = _generate_password()

    user = User(
        email=email_norm,
        password=hash_password(plain_password),
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"[REGISTER EMAIL] email={user.email}")
    print(f"[REGISTER PASSWORD] password={plain_password}")

    return user


def reset_password(db: Session, email: str) -> bool:
    email_norm = _norm_email(email)
    user = db.query(User).filter(User.email == email_norm).first()
    if not user:
        return False

    plain_password = _generate_password()
    user.password = hash_password(plain_password)

    db.add(user)
    db.commit()

    print(f"[RESET EMAIL] email={user.email}")
    print(f"[RESET PASSWORD] password={plain_password}")

    return True


def login_user(db: Session, email: str, password: str) -> str | None:
    email_norm = _norm_email(email)
    user = db.query(User).filter(User.email == email_norm).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None

    return create_access_token(user_id=user.id)


def update_user_profile(db: Session, user: User, data: UserUpdate) -> User:
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.patronymic is not None:
        user.patronymic = data.patronymic

    if data.password is not None and data.password.strip():
        user.password = hash_password(data.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user_account(db: Session, user: User, password: str) -> bool:
    if not verify_password(password, user.password):
        return False

    db.delete(user)
    db.commit()
    return True
