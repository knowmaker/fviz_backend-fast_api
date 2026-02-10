# app/models/system_type.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class SystemType(Base):
    __tablename__ = "system_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    orderliness = Column(String, nullable=False)

    quantities = relationship("Quantity", back_populates="system_type")
    laws = relationship("Law", back_populates="system_type")
    represents = relationship("Represent", back_populates="system_type")
    gk_groups = relationship("GK", back_populates="system_type")
    law_groups = relationship("LawGroup", back_populates="system_type")
