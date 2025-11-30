# app/api/v1/lt.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.dependencies import get_db
from app.schemas.lt import LTRead
from app.services.lt_service import get_all_lt

router = APIRouter()


@router.get("/", response_model=List[LTRead])
def read_all_lt(db: Session = Depends(get_db)):
    """
    Получить все записи из таблицы lt.
    Маршрут: GET /lt
    """
    return get_all_lt(db)
