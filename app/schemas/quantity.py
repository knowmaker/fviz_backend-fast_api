# app/schemas/quantity.py
from decimal import Decimal
from pydantic import BaseModel, Field

from app.schemas.lt import LTRead
from app.schemas.gk import GKRead


class QuantityRead(BaseModel):
    id: int
    symbol: str
    name: str
    unit: str

    m_indicate_auto: Decimal
    l_indicate_auto: Decimal
    t_indicate_auto: Decimal
    i_indicate_auto: Decimal

    lt_id: int
    gk_id: int
    system_type_id: int

    class Config:
        from_attributes = True


class QuantityReadWithLTGK(QuantityRead):
    lt: LTRead
    gk: GKRead


class QuantityCreate(BaseModel):
    symbol: str = Field(max_length=255)
    name: str = Field(max_length=255)
    unit: str = Field(max_length=255)

    m_indicate_auto: Decimal
    l_indicate_auto: Decimal
    t_indicate_auto: Decimal
    i_indicate_auto: Decimal

    lt_id: int
    gk_id: int
    system_type_id: int


class QuantityUpdate(BaseModel):
    symbol: str | None = Field(default=None, max_length=255)
    name: str | None = Field(default=None, max_length=255)
    unit: str | None = Field(default=None, max_length=255)

    m_indicate_auto: Decimal | None = None
    l_indicate_auto: Decimal | None = None
    t_indicate_auto: Decimal | None = None
    i_indicate_auto: Decimal | None = None

    lt_id: int | None = None
    gk_id: int | None = None
