# app/schemas/lt.py
from pydantic import BaseModel


class SystemTypeRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
