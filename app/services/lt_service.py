# app/services/lt_service.py
from sqlalchemy.orm import Session

from app.models.lt import LT


def get_all_lt(db: Session) -> list[LT]:
    """
    Возвращает все записи из таблицы lt.
    """
    return db.query(LT).all()
