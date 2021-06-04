from typing import Any, Dict

from sqlalchemy.orm import Session

from app.db_models.cart import Cart
from app.tests.factory.base import Base


class CartFactory(Base):
    def __init__(self, item_id: int, shop_id: int, user_id: int) -> None:
        self.id = None
        self.item_id = item_id
        self.shop_id = shop_id
        self.user_id = user_id
        self.item_quantity = None

    def create(self, db: Session):
        cart_item = Cart(item_id=self.item_id, shop_id=self.shop_id, user_id=self.user_id)
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        self.id = cart_item.id
        self.item_quantity = cart_item.item_quantity

    def update(self, db: Session, values: Dict[str, Any]):
        cart_item: Cart = db.query(Cart).filter_by(item_id=self.item_id).first()
        for key in values:
            setattr(cart_item, key, values[key])
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        for key in values:
            setattr(self, key, getattr(cart_item, key))

    @staticmethod
    def get_by_item_id(db: Session, item_id: int) -> Cart:
        return db.query(Cart).filter_by(item_id=item_id).first()
