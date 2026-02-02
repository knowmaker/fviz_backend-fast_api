# app/services/law_service.py
from sqlalchemy.orm import Session

from app.models.law import Law
from app.schemas.law import LawCreate, LawUpdate


def get_user_laws_by_system_type(db: Session, user_id: int, system_type_id: int) -> list[Law]:
    return (
        db.query(Law)
        .filter(Law.user_id == user_id, Law.system_type_id == system_type_id)
        .order_by(Law.id.asc())
        .all()
    )


def get_user_law_by_id(db: Session, user_id: int, law_id: int) -> Law | None:
    return db.query(Law).filter(Law.user_id == user_id, Law.id == law_id).first()


def create_user_law(db: Session, user_id: int, data: LawCreate) -> Law:
    law = Law(
        name=data.name,
        first_quantity_id=data.first_quantity_id,
        second_quantity_id=data.second_quantity_id,
        third_quantity_id=data.third_quantity_id,
        fourth_quantity_id=data.fourth_quantity_id,
        user_id=user_id,
        law_group_id=data.law_group_id,
        system_type_id=data.system_type_id,
    )
    db.add(law)
    db.commit()
    db.refresh(law)
    return law


def update_user_law(db: Session, user_id: int, law_id: int, data: LawUpdate) -> Law | None:
    law = get_user_law_by_id(db, user_id=user_id, law_id=law_id)
    if not law:
        return None

    if data.name is not None:
        law.name = data.name

    if data.law_group_id is not None:
        law.law_group_id = data.law_group_id

    db.add(law)
    db.commit()
    db.refresh(law)
    return law


def delete_user_law(db: Session, user_id: int, law_id: int) -> bool:
    law = get_user_law_by_id(db, user_id=user_id, law_id=law_id)
    if not law:
        return False

    db.delete(law)
    db.commit()
    return True
