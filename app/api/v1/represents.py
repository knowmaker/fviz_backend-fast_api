# app/api/v1/represents.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.represent import RepresentRead, RepresentCreate, RepresentUpdate
from app.services.represent_service import (
    get_user_represents,
    get_user_represent_by_id,
    create_user_represent,
    update_user_represent,
    delete_user_represent,
)

router = APIRouter()


@router.get("/", response_model=list[RepresentRead])
def read_my_represents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_represents(db, user_id=current_user.id)


@router.get("/{represent_id}", response_model=RepresentRead)
def read_my_represent_by_id(
    represent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rep = get_user_represent_by_id(db, user_id=current_user.id, represent_id=represent_id)
    if not rep:
        raise HTTPException(status_code=404, detail="Represent not found")
    return rep


@router.post("/", response_model=RepresentRead, status_code=status.HTTP_201_CREATED)
def create_my_represent(
    payload: RepresentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    create_user_represent(db, user_id=current_user.id, data=payload)


@router.patch("/{represent_id}", response_model=RepresentRead)
def update_my_represent(
    represent_id: int,
    payload: RepresentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rep = update_user_represent(
        db,
        user_id=current_user.id,
        represent_id=represent_id,
        data=payload,
    )
    if not rep:
        raise HTTPException(status_code=404, detail="Represent not found")
    return rep


@router.delete("/{represent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_represent(
    represent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = delete_user_represent(db, user_id=current_user.id, represent_id=represent_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Represent not found")
    return None
