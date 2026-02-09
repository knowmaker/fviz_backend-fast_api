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

    m_indicate: Decimal
    l_indicate: Decimal
    t_indicate: Decimal
    i_indicate: Decimal

    lt_id: int
    gk_id: int
    system_type_id: int

    class Config:
        from_attributes = True


class QuantityReadWithLTGK(QuantityRead):
    lt: LTRead
    gk: GKRead


class QuantityCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)
    unit: str = Field(min_length=1, max_length=255)

    m_indicate: Decimal
    l_indicate: Decimal
    t_indicate: Decimal
    i_indicate: Decimal

    lt_id: int
    gk_id: int
    system_type_id: int


class QuantityUpdate(BaseModel):
    symbol: str | None = Field(default=None, max_length=255)
    name: str | None = Field(default=None, max_length=255)
    unit: str | None = Field(default=None, max_length=255)

    m_indicate: Decimal | None = None
    l_indicate: Decimal | None = None
    t_indicate: Decimal | None = None
    i_indicate: Decimal | None = None

    lt_id: int | None = None
    gk_id: int | None = None
