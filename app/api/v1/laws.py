# app/api/v1/laws.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.law import LawCreate, LawUpdate, LawRead
from app.services.law_service import (
    get_user_laws_by_system_type,
    get_user_law_by_id,
    create_user_law,
    update_user_law,
    delete_user_law,
)

router = APIRouter()


@router.get("/by-system-type/{system_type_id}", response_model=list[LawRead])
def read_my_laws_by_system_type(
    system_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_laws_by_system_type(db, user_id=current_user.id, system_type_id=system_type_id)


@router.get("/{law_id}", response_model=LawRead)
def read_my_law_by_id(
    law_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    law = get_user_law_by_id(db, user_id=current_user.id, law_id=law_id)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")
    return law


@router.post("/", response_model=LawRead, status_code=status.HTTP_201_CREATED)
def create_my_law(
    payload: LawCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_user_law(db, user_id=current_user.id, data=payload)


@router.patch("/{law_id}", response_model=LawRead)
def update_my_law(
    law_id: int,
    payload: LawUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    law = update_user_law(db, user_id=current_user.id, law_id=law_id, data=payload)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")
    return law


@router.delete("/{law_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_law(
    law_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = delete_user_law(db, user_id=current_user.id, law_id=law_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Law not found")
    return None
