# app/api/v1/law_groups.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.law_group import LawGroupCreate, LawGroupUpdate, LawGroupRead
from app.services.law_group_service import (
    get_all_law_groups_by_system_type,
    get_law_group_by_id,
    create_law_group,
    update_law_group,
    delete_law_group,
)

router = APIRouter()


@router.get("/by-system-type/{system_type_id}", response_model=list[LawGroupRead])
def read_all_law_groups_by_system_type(
        system_type_id: int,
        db: Session = Depends(get_db)
):
    return get_all_law_groups_by_system_type(db, system_type_id=system_type_id)


@router.get("/{law_group_id}", response_model=LawGroupRead)
def read_law_group(law_group_id: int, db: Session = Depends(get_db)):
    lg = get_law_group_by_id(db, law_group_id=law_group_id)
    if not lg:
        raise HTTPException(status_code=404, detail="LawGroup not found")
    return lg


@router.post("/", response_model=LawGroupRead, status_code=status.HTTP_201_CREATED)
def create_law_group_endpoint(
    payload: LawGroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_law_group(db, data=payload)


@router.patch("/{law_group_id}", response_model=LawGroupRead)
def update_law_group_endpoint(
    law_group_id: int,
    payload: LawGroupUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lg = update_law_group(db, law_group_id=law_group_id, data=payload)
    if not lg:
        raise HTTPException(status_code=404, detail="LawGroup not found")
    return lg


@router.delete("/{law_group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_law_group_endpoint(
    law_group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = delete_law_group(db, law_group_id=law_group_id)
    if not ok:
        raise HTTPException(status_code=404, detail="LawGroup not found")
    return None
