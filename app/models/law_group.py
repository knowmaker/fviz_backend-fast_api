# app/models/law_group.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class LawGroup(Base):
    __tablename__ = "law_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    color = Column(String(7), nullable=False)  # "#RRGGBB"

    system_type_id = Column(
        Integer,
        ForeignKey("system_types.id"),
        nullable=False,
        index=True,
    )

    system_type = relationship("SystemType", back_populates="law_groups")
    laws = relationship("Law", back_populates="law_group")
