# app/services/quantity_service.py
from sqlalchemy.orm import Session, joinedload

from app.models.quantity import Quantity
from app.schemas.quantity import QuantityCreate, QuantityUpdate


def get_quantities_by_system_type_by_lt_id(db: Session, system_type_id: int, lt_id: int) -> list[Quantity]:
    return (
        db.query(Quantity)
        .options(joinedload(Quantity.gk))
        .filter(Quantity.lt_id == lt_id, Quantity.system_type_id == system_type_id)
        .order_by(Quantity.id.asc())
        .all()
    )


def get_quantity_by_id(db: Session, quantity_id: int) -> Quantity | None:
    return (
        db.query(Quantity)
        .options(joinedload(Quantity.lt), joinedload(Quantity.gk))
        .filter(Quantity.id == quantity_id)
        .first()
    )


def create_quantity(db: Session, data: QuantityCreate) -> Quantity:
    q = Quantity(
        symbol=data.symbol,
        name=data.name,
        unit=data.unit,
        m_indicate=data.m_indicate,
        l_indicate=data.l_indicate,
        t_indicate=data.t_indicate,
        i_indicate=data.i_indicate,
        lt_id=data.lt_id,
        gk_id=data.gk_id,
        system_type_id=data.system_type_id,
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def update_quantity(db: Session, quantity_id: int, data: QuantityUpdate) -> Quantity | None:
    q = db.query(Quantity).filter(Quantity.id == quantity_id).first()
    if not q:
        return None

    # обновляем любые поля, кроме system_type_id
    if data.symbol is not None:
        q.symbol = data.symbol
    if data.name is not None:
        q.name = data.name
    if data.unit is not None:
        q.unit = data.unit

    if data.m_indicate is not None:
        q.m_indicate = data.m_indicate
    if data.l_indicate is not None:
        q.l_indicate = data.l_indicate
    if data.t_indicate is not None:
        q.t_indicate = data.t_indicate
    if data.i_indicate is not None:
        q.i_indicate = data.i_indicate

    if data.lt_id is not None:
        q.lt_id = data.lt_id
    if data.gk_id is not None:
        q.gk_id = data.gk_id

    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def delete_quantity(db: Session, quantity_id: int) -> bool:
    q = db.query(Quantity).filter(Quantity.id == quantity_id).first()
    if not q:
        return False

    db.delete(q)
    db.commit()
    return True
