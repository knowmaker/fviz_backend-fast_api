# app/deps/dependencies.py
from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Зависимость FastAPI для получения сессии БД.
    Открывает сессию перед обработкой запроса и закрывает после.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
