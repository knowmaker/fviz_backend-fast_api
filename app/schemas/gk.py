# app/schemas/gk.py
from pydantic import BaseModel, Field


HEX_COLOR_RE = r"^#[0-9a-fA-F]{6}$"


class GKRead(BaseModel):
    id: int
    g_indicate: int
    k_indicate: int
    name: str
    color: str
    system_type_id: int

    class Config:
        from_attributes = True


class GKUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    color: str | None = Field(default=None, pattern=HEX_COLOR_RE)
