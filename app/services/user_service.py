# app/services/user_service.py
import secrets
import string
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.core.email import send_email
from app.core.config import settings
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

    subject = f"{settings.PROJECT_NAME}: регистрация"
    body = (
        f"Здравствуйте!\n\n"
        f"Вы зарегистрированы в {settings.PROJECT_NAME}.\n"
        f"Ваш пароль: {plain_password}\n\n"
        f"Если это были не вы — просто проигнорируйте письмо."
    )

    try:
        send_email(to_email=user.email, subject=subject, body=body)
    except Exception as e:
        raise RuntimeError("Failed to send registration email") from e

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def reset_password(db: Session, email: str) -> bool:
    email_norm = _norm_email(email)
    user = db.query(User).filter(User.email == email_norm).first()
    if not user:
        return False

    plain_password = _generate_password()
    new_hash = hash_password(plain_password)

    subject = f"{settings.PROJECT_NAME}: восстановление пароля"
    body = (
        f"Здравствуйте!\n\n"
        f"Ваш пароль был сброшен для {settings.PROJECT_NAME}.\n"
        f"Новый пароль: {plain_password}\n\n"
        f"Если это были не вы — срочно смените пароль после входа."
    )

    try:
        send_email(to_email=user.email, subject=subject, body=body)
    except Exception as e:
        raise RuntimeError("Failed to send reset password email") from e

    user.password = new_hash
    db.add(user)
    db.commit()
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