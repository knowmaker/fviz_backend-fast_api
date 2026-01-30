# app/api/v1/gk.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.gk import GKCreate, GKUpdate, GKRead
from app.services.gk_service import (
    get_gk_by_system_type,
    get_gk_by_id,
    create_gk,
    update_gk,
    delete_gk,
)

router = APIRouter()


@router.get("/by-system-type/{system_type_id}", response_model=list[GKRead])
def read_gk_by_system_type_endpoint(
    system_type_id: int,
    db: Session = Depends(get_db),
):
    return get_gk_by_system_type(db, system_type_id=system_type_id)


@router.get("/{gk_id}", response_model=GKRead)
def read_gk_by_id_endpoint(
    gk_id: int,
    db: Session = Depends(get_db),
):
    gk = get_gk_by_id(db, gk_id=gk_id)
    if not gk:
        raise HTTPException(status_code=404, detail="GK not found")
    return gk


@router.post("/", response_model=GKRead, status_code=status.HTTP_201_CREATED)
def create_gk_endpoint(
    payload: GKCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_gk(db, data=payload)


@router.patch("/{gk_id}", response_model=GKRead)
def update_gk_endpoint(
    gk_id: int,
    payload: GKUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    gk = update_gk(db, gk_id=gk_id, data=payload)
    if not gk:
        raise HTTPException(status_code=404, detail="GK not found")
    return gk


@router.delete("/{gk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gk_endpoint(
    gk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = delete_gk(db, gk_id=gk_id)
    if not ok:
        raise HTTPException(status_code=404, detail="GK not found")
    return None
