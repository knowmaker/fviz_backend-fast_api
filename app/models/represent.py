# app/models/represent.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class Represent(Base):
    __tablename__ = "represents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    system_type_id = Column(
        Integer,
        ForeignKey("system_types.id"),
        nullable=False,
        index=True,
    )
    is_active = Column(Boolean, default=True, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    updated_at = Column(DateTime(timezone=True), nullable=True)
    system_type = relationship("SystemType", back_populates="represents")
    user = relationship("User", back_populates="represents")

    quantities = relationship(
        "Quantity",
        secondary="quantities_in_represents",
        back_populates="represents",
    )
