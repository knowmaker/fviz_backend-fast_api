# app/models/law.py
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.db.base import Base


class Law(Base):
    __tablename__ = "laws"

    __table_args__ = (
        UniqueConstraint("user_id", "quantity_ids_sorted", name="uq_laws_user_sorted_array"),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    first_quantity_id = Column(Integer, ForeignKey("quantities.id"), nullable=False)
    second_quantity_id = Column(Integer, ForeignKey("quantities.id"), nullable=False)
    third_quantity_id = Column(Integer, ForeignKey("quantities.id"), nullable=False)
    fourth_quantity_id = Column(Integer, ForeignKey("quantities.id"), nullable=False)
    quantity_ids_sorted = Column(ARRAY(Integer), nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    law_group_id = Column(
        Integer,
        ForeignKey("law_groups.id"),
        nullable=True,
        index=True,
    )
    system_type_id = Column(
        Integer,
        ForeignKey("system_types.id"),
        nullable=False,
        index=True,
    )

    first_quantity = relationship(
        "Quantity",
        foreign_keys=[first_quantity_id],
        back_populates="laws_first",
    )
    second_quantity = relationship(
        "Quantity",
        foreign_keys=[second_quantity_id],
        back_populates="laws_second",
    )
    third_quantity = relationship(
        "Quantity",
        foreign_keys=[third_quantity_id],
        back_populates="laws_third",
    )
    fourth_quantity = relationship(
        "Quantity",
        foreign_keys=[fourth_quantity_id],
        back_populates="laws_fourth",
    )

    user = relationship("User", back_populates="laws")
    law_group = relationship("LawGroup", back_populates="laws")
    system_type = relationship("SystemType", back_populates="laws")
