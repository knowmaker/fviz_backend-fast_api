# app/schemas/quantity.py
from pydantic import BaseModel, Field

from app.schemas.lt import LTRead
from app.schemas.gk import GKRead

# Разрешаем: -2, 0, 10, 1/2, -3/4
FRACTION_RE = r"^-?(?:100|[1-9]?\d)(?:/(?:100|[1-9]?\d))?$"


class QuantityRead(BaseModel):
    id: int
    symbol: str
    name: str
    unit: str

    m_indicate: str
    l_indicate: str
    t_indicate: str
    i_indicate: str

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

    m_indicate: str = Field(pattern=FRACTION_RE)
    l_indicate: str = Field(pattern=FRACTION_RE)
    t_indicate: str = Field(pattern=FRACTION_RE)
    i_indicate: str = Field(pattern=FRACTION_RE)

    lt_id: int
    gk_id: int
    system_type_id: int


class QuantityUpdate(BaseModel):
    symbol: str | None = Field(default=None, min_length=1, max_length=255)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    unit: str | None = Field(default=None, min_length=1, max_length=255)

    m_indicate: str | None = Field(default=None, pattern=FRACTION_RE)
    l_indicate: str | None = Field(default=None, pattern=FRACTION_RE)
    t_indicate: str | None = Field(default=None, pattern=FRACTION_RE)
    i_indicate: str | None = Field(default=None, pattern=FRACTION_RE)

    lt_id: int | None = None
    gk_id: int | None = None
