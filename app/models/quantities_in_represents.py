# app/models/quantities_in_represents.py
from sqlalchemy import Column, Integer, ForeignKey, Table

from app.db.base import Base

QuantitiesInRepresents = Table(
    "quantities_in_represents",
    Base.metadata,
    Column(
        "represent_id",
        Integer,
        ForeignKey("represents.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "quantity_id",
        Integer,
        ForeignKey("quantities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
