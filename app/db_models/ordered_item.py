from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relation

from app.db.base_class import Base


class OrderedItem(Base):
    __tablename__ = 'ordered_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    order = relation("Order", back_populates="ordered_items")
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    # Also saving cost because it can be changed later by the owner
    cost = Column(Numeric(asdecimal=True, scale=2), nullable=False)
