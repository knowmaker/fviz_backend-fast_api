# app/services/represent_service.py
from sqlalchemy.orm import Session

from app.models.represent import Represent
from app.models.quantity import Quantity
from app.schemas.represent import RepresentCreate, RepresentUpdate


def get_user_represents(db: Session, user_id: int) -> list[Represent]:
    return (
        db.query(Represent)
        .filter(Represent.user_id == user_id)
        .order_by(Represent.id.asc())
        .all()
    )


def get_user_represent_by_id(db: Session, user_id: int, represent_id: int) -> Represent | None:
    return db.query(Represent).filter(Represent.user_id == user_id, Represent.id == represent_id).first()


def create_user_represent(db: Session, user_id: int, data: RepresentCreate) -> Represent:
    quantities = db.query(Quantity).filter(Quantity.id.in_(data.quantity_ids)).all()

    rep = Represent(
        title=data.title,
        system_type_id=data.system_type_id,
        is_active=data.is_active,
        is_public=data.is_public,
        user_id=user_id,
    )
    rep.quantities = quantities

    db.add(rep)
    db.commit()
    db.refresh(rep)
    return rep


def update_user_represent(db: Session, user_id: int, represent_id: int, data: RepresentUpdate) -> Represent | None:
    rep = get_user_represent_by_id(db, user_id=user_id, represent_id=represent_id)
    if not rep:
        return None

    if data.title is not None:
        rep.title = data.title

    if data.is_active is not None:
        rep.is_active = data.is_active

    if data.is_public is not None:
        rep.is_public = data.is_public

    if data.quantity_ids is not None:
        quantities = db.query(Quantity).filter(Quantity.id.in_(data.quantity_ids)).all()
        rep.quantities = quantities

    db.add(rep)
    db.commit()
    db.refresh(rep)
    return rep


def delete_user_represent(db: Session, user_id: int, represent_id: int) -> bool:
    rep = get_user_represent_by_id(db, user_id=user_id, represent_id=represent_id)
    if not rep:
        return False

    db.delete(rep)
    db.commit()
    return True
