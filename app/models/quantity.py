# app/models/quantity.py
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.db.base import Base


class Quantity(Base):
    __tablename__ = "quantities"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    name = Column(String, nullable=False)
    unit = Column(String, nullable=False)

    m_indicate_auto = Column(Numeric(4, 1), nullable=False)
    l_indicate_auto = Column(Numeric(4, 1), nullable=False)
    t_indicate_auto = Column(Numeric(4, 1), nullable=False)
    i_indicate_auto = Column(Numeric(4, 1), nullable=False)

    lt_id = Column(Integer, ForeignKey("lt.id"), nullable=False, index=True)
    gk_id = Column(Integer, ForeignKey("gk.id"), nullable=False, index=True)
    system_type_id = Column(
        Integer,
        ForeignKey("system_types.id"),
        nullable=False,
        index=True,
    )

    lt = relationship("LT", back_populates="quantities")
    gk = relationship("GK", back_populates="quantities")
    system_type = relationship("SystemType", back_populates="quantities")

    # связи с законами (через несколько FK)
    laws_first = relationship(
        "Law",
        back_populates="first_quantity",
        foreign_keys="Law.first_quantity_id",
    )
    laws_second = relationship(
        "Law",
        back_populates="second_quantity",
        foreign_keys="Law.second_quantity_id",
    )
    laws_third = relationship(
        "Law",
        back_populates="third_quantity",
        foreign_keys="Law.third_quantity_id",
    )
    laws_fourth = relationship(
        "Law",
        back_populates="fourth_quantity",
        foreign_keys="Law.fourth_quantity_id",
    )

    represents = relationship(
        "Represent",
        secondary="quantities_in_represents",
        back_populates="quantities",
    )
