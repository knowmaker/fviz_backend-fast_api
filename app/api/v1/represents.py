# app/api/v1/represents.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.dependencies import get_db, get_current_user, get_optional_current_user
from app.models.user import User
from app.schemas.represent import RepresentRead, RepresentCreate, RepresentUpdate, RepresentViewResponse
from app.services.represent_service import (
    get_user_represents_by_system_type,
    get_user_represent_by_id,
    create_user_represent,
    update_user_represent,
    delete_user_represent,
    get_active_view_for_user,
    get_active_view_for_user_by_system_type,
    get_active_view_public,
    get_active_view_public_by_system_type,
    get_view_by_represent_id_for_user,
)

router = APIRouter()


@router.get("/view", response_model=RepresentViewResponse)
def read_active_view(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    if current_user is not None:
        rep, quantities = get_active_view_for_user(db, user_id=current_user.id)
        if rep is not None:
            return RepresentViewResponse(represent=rep, quantities=quantities)

    rep, quantities = get_active_view_public(db)
    return RepresentViewResponse(represent=rep, quantities=quantities)


@router.get("/view/by-system-type/{system_type_id}", response_model=RepresentViewResponse)
def read_active_view_by_system_type(
    system_type_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    if current_user is not None:
        rep, quantities = get_active_view_for_user_by_system_type(
            db, user_id=current_user.id, system_type_id=system_type_id
        )
        if rep is not None:
            return RepresentViewResponse(represent=rep, quantities=quantities)

    rep, quantities = get_active_view_public_by_system_type(db, system_type_id=system_type_id)
    return RepresentViewResponse(represent=rep, quantities=quantities)


@router.get("/{represent_id}/view", response_model=RepresentViewResponse)
def read_represent_view_by_id(
    represent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = get_view_by_represent_id_for_user(db, user_id=current_user.id, represent_id=represent_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Represent not found")

    rep, quantities = result
    return RepresentViewResponse(represent=rep, quantities=quantities)


@router.get("/by-system-type/{system_type_id}", response_model=list[RepresentRead])
def read_my_represents_by_system_type(
    system_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_represents_by_system_type(db, user_id=current_user.id, system_type_id=system_type_id)


@router.post("/", response_model=RepresentRead, status_code=status.HTTP_201_CREATED)
def create_my_represent(
    payload: RepresentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_user_represent(db, user_id=current_user.id, data=payload)


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
