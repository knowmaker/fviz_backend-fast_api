# app/models/gk.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class GK(Base):
    __tablename__ = "gk"

    id = Column(Integer, primary_key=True, index=True)
    g_indicate = Column(String, nullable=False)
    k_indicate = Column(String, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String(7), nullable=False)  # формат "#RRGGBB"

    system_type_id = Column(
        Integer,
        ForeignKey("system_types.id"),
        nullable=False,
        index=True,
    )

    system_type = relationship("SystemType", back_populates="gk_groups")
    quantities = relationship("Quantity", back_populates="gk")
