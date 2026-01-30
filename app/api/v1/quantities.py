# app/api/v1/quantities.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.quantity import (
    QuantityCreate,
    QuantityUpdate,
    QuantityReadWithLTGK,
    QuantityReadWithGK,
    QuantityRead,
)
from app.services.quantity_service import (
    get_quantity_by_id,
    get_quantities_by_lt_id,
    create_quantity,
    update_quantity,
    delete_quantity,
)

router = APIRouter()


@router.get("/{quantity_id}", response_model=QuantityReadWithLTGK)
def read_quantity_by_id(
    quantity_id: int,
    db: Session = Depends(get_db),
):
    q = get_quantity_by_id(db, quantity_id=quantity_id)
    if not q:
        raise HTTPException(status_code=404, detail="Quantity not found")
    return q


@router.get("/by-lt/{lt_id}", response_model=list[QuantityReadWithGK])
def read_quantities_by_lt(
    lt_id: int,
    db: Session = Depends(get_db),
):
    return get_quantities_by_lt_id(db, lt_id=lt_id)


@router.post("/", response_model=QuantityRead, status_code=status.HTTP_201_CREATED)
def create_quantity_endpoint(
    payload: QuantityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_quantity(db, data=payload)


@router.patch("/{quantity_id}", response_model=QuantityRead)
def update_quantity_endpoint(
    quantity_id: int,
    payload: QuantityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = update_quantity(db, quantity_id=quantity_id, data=payload)
    if not q:
        raise HTTPException(status_code=404, detail="Quantity not found")
    return q


@router.delete("/{quantity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quantity_endpoint(
    quantity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = delete_quantity(db, quantity_id=quantity_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Quantity not found")
    return None
