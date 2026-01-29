# app/core/security.py
import hmac
import hashlib
import time
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int) -> str:
    """
    JWT на 1 неделю.
    sub хранит user_id.
    """
    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=settings.JWT_EXPIRE_SECONDS)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as e:
        raise ValueError("Invalid token") from e


def _time_counter(ttl_seconds: int) -> int:
    """
    Счётчик временных окон: каждые ttl_seconds — новое окно.
    """
    return int(time.time()) // ttl_seconds


def generate_confirmation_code(email: str) -> str:
    """
    6-значный код без хранения.
    Детерминированный по (SECRET_KEY + purpose + email + текущее окно).
    """
    email_norm = email.strip().lower()
    counter = _time_counter(settings.CONFIRM_CODE_TTL_SECONDS)

    msg = f"confirm:{email_norm}:{counter}".encode("utf-8")
    key = settings.SECRET_KEY.encode("utf-8")

    digest = hmac.new(key, msg, hashlib.sha256).digest()
    num = int.from_bytes(digest[:4], "big") % 1_000_000
    return f"{num:06d}"


def verify_confirmation_code(email: str, code: str) -> bool:
    """
    Проверяем в текущем и предыдущем окне (на случай рассинхрона времени).
    """
    email_norm = email.strip().lower()
    code_norm = code.strip()

    if len(code_norm) != 6 or not code_norm.isdigit():
        return False

    ttl = settings.CONFIRM_CODE_TTL_SECONDS
    current = _time_counter(ttl)

    for c in (current, current - 1):
        msg = f"confirm:{email_norm}:{c}".encode("utf-8")
        key = settings.SECRET_KEY.encode("utf-8")
        digest = hmac.new(key, msg, hashlib.sha256).digest()
        num = int.from_bytes(digest[:4], "big") % 1_000_000
        expected = f"{num:06d}"
        if hmac.compare_digest(expected, code_norm):
            return True

    return False
