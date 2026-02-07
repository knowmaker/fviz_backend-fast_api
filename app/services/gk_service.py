# app/services/gk_service.py
from sqlalchemy.orm import Session

from app.models.gk import GK
from app.schemas.gk import GKUpdate


def get_gk_by_system_type(db: Session, system_type_id: int) -> list[GK]:
    return (
        db.query(GK)
        .filter(GK.system_type_id == system_type_id)
        .order_by(GK.id.asc())
        .all()
    )


def get_gk_by_id(db: Session, gk_id: int) -> GK | None:
    return db.query(GK).filter(GK.id == gk_id).first()



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
