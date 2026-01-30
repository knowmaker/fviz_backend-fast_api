# app/schemas/law_group.py
from pydantic import BaseModel, Field


HEX_COLOR_RE = r"^#[0-9a-fA-F]{6}$"


class LawGroupRead(BaseModel):
    id: int
    name: str
    color: str
    system_type_id: int

    class Config:
        from_attributes = True


class LawGroupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    color: str = Field(pattern=HEX_COLOR_RE)
    system_type_id: int


class LawGroupUpdate(BaseModel):
    # обновляем только name и color
    name: str | None = Field(default=None, min_length=1, max_length=255)
    color: str | None = Field(default=None, pattern=HEX_COLOR_RE)
