# app/services/law_group_service.py
from sqlalchemy.orm import Session

from app.models.law_group import LawGroup
from app.schemas.law_group import LawGroupCreate, LawGroupUpdate


def get_all_law_groups_by_system_type(db: Session, system_type_id: int) -> list[LawGroup]:
    return (
        db.query(LawGroup)
        .filter(LawGroup.system_type_id == system_type_id)
        .order_by(LawGroup.id.asc())
        .all()
    )


def get_law_group_by_id(db: Session, law_group_id: int) -> LawGroup | None:
    return db.query(LawGroup).filter(LawGroup.id == law_group_id).first()


def create_law_group(db: Session, data: LawGroupCreate) -> LawGroup:
    lg = LawGroup(
        name=data.name,
        color=data.color,
        system_type_id=data.system_type_id,
    )
    db.add(lg)
    db.commit()
    db.refresh(lg)
    return lg


def update_law_group(db: Session, law_group_id: int, data: LawGroupUpdate) -> LawGroup | None:
    lg = get_law_group_by_id(db, law_group_id=law_group_id)
    if not lg:
        return None

    if data.name is not None:
        lg.name = data.name
    if data.color is not None:
        lg.color = data.color

    db.add(lg)
    db.commit()
    db.refresh(lg)
    return lg


def delete_law_group(db: Session, law_group_id: int) -> bool:
    lg = get_law_group_by_id(db, law_group_id=law_group_id)
    if not lg:
        return False

    db.delete(lg)
    db.commit()
    return True
