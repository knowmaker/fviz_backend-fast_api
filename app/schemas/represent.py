# app/schemas/represent.py
from pydantic import BaseModel, Field

from app.schemas.quantity import QuantityRead

class RepresentRead(BaseModel):
    id: int
    title: str
    system_type_id: int
    is_active: bool
    is_public: bool
    user_id: int

    class Config:
        from_attributes = True


class RepresentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    system_type_id: int
    is_active: bool = True
    is_public: bool = False
    quantity_ids: list[int] = Field(min_length=1)


class RepresentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = None
    is_public: bool | None = None
    quantity_ids: list[int] | None = Field(default=None, min_length=1)


class RepresentViewResponse(BaseModel):
    represent: RepresentRead | None
    quantities: list[QuantityRead]
