# app/models/lt.py
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base


class LT(Base):
    __tablename__ = "lt"

    id = Column(Integer, primary_key=True, index=True)
    l_indicate = Column(Integer, nullable=False)
    t_indicate = Column(Integer, nullable=False)

    quantities = relationship("Quantity", back_populates="lt")
