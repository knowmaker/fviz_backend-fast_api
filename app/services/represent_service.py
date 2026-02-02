# app/services/represent_service.py
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.represent import Represent
from app.models.quantity import Quantity
from app.schemas.represent import RepresentCreate, RepresentUpdate


def get_user_represents_by_system_type(db: Session, user_id: int, system_type_id: int) -> list[Represent]:
    return (
        db.query(Represent)
        .filter(Represent.user_id == user_id, Represent.system_type_id == system_type_id)
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

def get_active_view_for_user(db: Session, user_id: int) -> tuple[Represent | None, list[Quantity]]:
    rep = (
        db.query(Represent)
        .filter(Represent.user_id == user_id, Represent.is_active.is_(True))
        .order_by(Represent.id.desc())
        .first()
    )
    if not rep:
        return None, []
    return rep, list(rep.quantities)

def get_active_view_public(db: Session) -> tuple[Represent, list[Quantity]]:
    system_type_id = (
        db.query(Quantity.system_type_id)
        .group_by(Quantity.system_type_id)
        .order_by(func.random())
        .limit(1)
        .scalar()
    )

    quantities = (
        db.query(Quantity)
        .filter(Quantity.system_type_id == system_type_id)
        .distinct(Quantity.lt_id)
        .order_by(Quantity.lt_id.asc(), func.random())
        .all()
    )

    data = {
        "id": 0,
        "title": "Случайное",
        "system_type_id": system_type_id,
        "is_active": False,
        "user_id": 0,
    }
    return data, quantities

def get_view_by_represent_id_for_user(
    db: Session,
    user_id: int,
    represent_id: int,
) -> tuple[Represent | None, list[Quantity]] | None:
    rep = get_user_represent_by_id(db, user_id=user_id, represent_id=represent_id)
    if not rep:
        return None
    return rep, list(rep.quantities)