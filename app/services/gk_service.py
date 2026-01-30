# app/services/gk_service.py
from sqlalchemy.orm import Session

from app.models.gk import GK
from app.schemas.gk import GKCreate, GKUpdate


def get_gk_by_system_type(db: Session, system_type_id: int) -> list[GK]:
    return (
        db.query(GK)
        .filter(GK.system_type_id == system_type_id)
        .order_by(GK.id.asc())
        .all()
    )


def get_gk_by_id(db: Session, gk_id: int) -> GK | None:
    return db.query(GK).filter(GK.id == gk_id).first()


def create_gk(db: Session, data: GKCreate) -> GK:
    gk = GK(
        g_indicate=data.g_indicate,
        k_indicate=data.k_indicate,
        name=data.name,
        color=data.color,
        system_type_id=data.system_type_id,
    )
    db.add(gk)
    db.commit()
    db.refresh(gk)
    return gk


def update_gk(db: Session, gk_id: int, data: GKUpdate) -> GK | None:
    gk = get_gk_by_id(db, gk_id)
    if not gk:
        return None

    if data.name is not None:
        gk.name = data.name
    if data.color is not None:
        gk.color = data.color

    db.add(gk)
    db.commit()
    db.refresh(gk)
    return gk


def delete_gk(db: Session, gk_id: int) -> bool:
    gk = get_gk_by_id(db, gk_id)
    if not gk:
        return False

    db.delete(gk)
    db.commit()
    return True
