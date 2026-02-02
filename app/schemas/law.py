# app/schemas/laws.py
from pydantic import BaseModel, Field


class LawRead(BaseModel):
    id: int
    name: str

    first_quantity_id: int
    second_quantity_id: int
    third_quantity_id: int
    fourth_quantity_id: int

    law_group_id: int
    system_type_id: int

    class Config:
        from_attributes = True


class LawCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)

    first_quantity_id: int
    second_quantity_id: int
    third_quantity_id: int
    fourth_quantity_id: int

    law_group_id: int
    system_type_id: int


class LawQuantitiesUpdate(BaseModel):
    """
    ВСПОМОГАТЕЛЬНАЯ схема:
    либо все 4 quantity_id, либо объект отсутствует целиком
    """
    first_quantity_id: int
    second_quantity_id: int
    third_quantity_id: int
    fourth_quantity_id: int


class LawUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    law_group_id: int | None = None

    quantities: LawQuantitiesUpdate | None = None
