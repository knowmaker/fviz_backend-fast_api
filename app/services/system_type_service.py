# app/services/lt_service.py
from sqlalchemy.orm import Session

from app.models.system_type import SystemType


def get_all_system_types(db: Session) -> list[SystemType]:
    return db.query(SystemType).all()
