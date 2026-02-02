# app/api/v1/lt.py
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps.dependencies import get_db
from app.schemas.system_type import SystemTypeRead
from app.services.system_type_service import get_all_system_types

router = APIRouter()


@router.get("/", response_model=List[SystemTypeRead])
def read_all_system_types(db: Session = Depends(get_db)):
    return get_all_system_types(db)
