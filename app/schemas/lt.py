# app/schemas/lt.py
from pydantic import BaseModel


class LTRead(BaseModel):
    id: int
    l_indicate: int
    t_indicate: int

    class Config:
        # Позволяет отдавать ORM-объекты (SQLAlchemy) напрямую в виде этой схемы
        from_attributes = True  # для Pydantic v2; для v1 было бы orm_mode = True
