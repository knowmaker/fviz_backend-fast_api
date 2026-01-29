# app/services/user_service.py
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_confirmation_code,
    verify_confirmation_code,
)
from app.models.user import User
from app.schemas.user import UserUpdate


def _norm_email(email: str) -> str:
    return email.strip().lower()


def register_user(db: Session, email: str, password: str) -> User:
    """
    Создаёт пользователя с is_confirmed=False и печатает код в консоль.

    Если пользователь уже существует:
      - confirmed=True  -> ошибка
      - confirmed=False -> "переотправка" кода (печатаем заново), пользователя не меняем
    """
    email_norm = _norm_email(email)
    existing = db.query(User).filter(User.email == email_norm).first()

    if existing:
        if existing.is_confirmed:
            raise ValueError("User already registered and confirmed")

        code = generate_confirmation_code(existing.email)
        print(f"[CONFIRM CODE] email={existing.email} code={code}")
        return existing

    user = User(
        email=email_norm,
        password=hash_password(password),
        is_confirmed=False,
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    code = generate_confirmation_code(user.email)
    print(f"[CONFIRM CODE] email={user.email} code={code}")

    return user


def confirm_user(db: Session, email: str, code: str) -> bool:
    """
    Подтверждает пользователя, если код верный.
    Код не храним: валидируем через HMAC.
    """
    email_norm = _norm_email(email)
    user = db.query(User).filter(User.email == email_norm).first()
    if not user:
        return False

    if user.is_confirmed:
        return True

    if not verify_confirmation_code(user.email, code):
        return False

    user.is_confirmed = True
    db.add(user)
    db.commit()
    return True


def login_user(db: Session, email: str, password: str) -> str | None:
    """
    Возвращает JWT, если:
      - пользователь существует
      - пароль верный
      - пользователь подтверждён
    """
    email_norm = _norm_email(email)
    user = db.query(User).filter(User.email == email_norm).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    if not user.is_confirmed:
        return None

    return create_access_token(user_id=user.id)


def update_user_profile(db: Session, user: User, data: UserUpdate) -> User:
    """
    Обновляем профиль (email нельзя).
    Если password передан — меняем пароль.
    """
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
