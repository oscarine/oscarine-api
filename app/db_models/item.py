from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relation

from app.choices.cost_unit import COST_UNIT_TYPES
from app.db.base_class import Base
from sqlalchemy_utils.types.choice import ChoiceType


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=40), nullable=False)
    cost = Column(Numeric(asdecimal=True, scale=2), nullable=False)
    cost_unit = Column(ChoiceType(COST_UNIT_TYPES), nullable=False)
    category = Column(String(length=25))
    order_count = Column(Integer, default=0)
    item_available = Column(Boolean, default=True)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    shop = relation("Shop", back_populates="items")
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    owner = relation("Owner", back_populates="items")
