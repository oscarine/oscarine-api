from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import relation

from app.db.base_class import Base
from app.db_models.ordered_item import OrderedItem
from sqlalchemy_utils import aggregated


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    order_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    ordered_items = relation("OrderedItem", back_populates="order")
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relation("User", back_populates="orders")
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    shop = relation("Shop", back_populates="orders")
    user_instructions = Column(String(length=150))

    @aggregated('ordered_items', Column(Numeric(asdecimal=True, scale=2)))
    def total_cost(self):
        return func.sum(OrderedItem.cost)

    # Order status
    accepted = Column(Boolean, default=False)  # For shops
    declined = Column(Boolean, default=False)  # For shops, can't decline once accepted
    canceled = Column(Boolean, default=False)  # For users
    delivered = Column(Boolean, default=False)
