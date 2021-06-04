from typing import List, Tuple

from sqlalchemy.orm import Session

from app.db_models.cart import Cart
from app.db_models.item import Item
from app.models.cart import CartUpdateChoiceEnum, UpdateCartItem


def add_cart_item(
    db_session: Session, user_id: int, shop_id: int, item_id: int
) -> Cart:
    cart_item = Cart(item_id=item_id, user_id=user_id, shop_id=shop_id)
    db_session.add(cart_item)
    db_session.commit()
    db_session.refresh(cart_item)
    return cart_item


def get_cart_item(db_session: Session, user_id: int, item_id: int) -> Cart:
    return db_session.query(Cart).filter_by(user_id=user_id, item_id=item_id).first()


def update_cart_item(db_session: Session, cart_item: Cart, data: UpdateCartItem):
    if data.action == CartUpdateChoiceEnum.minus and cart_item.item_quantity >= 1:
        cart_item.item_quantity = cart_item.item_quantity - 1
    elif data.action == CartUpdateChoiceEnum.plus:
        cart_item.item_quantity = cart_item.item_quantity + 1
    db_session.add(cart_item)
    db_session.commit()
    return cart_item


def get_cart_items_detailed(
    db_session: Session, user_id: int
) -> List[Tuple[Cart, Item]]:
    return db_session.query(Cart, Item).filter(Cart.user_id == user_id).join(Item).all()


def delete_cart_item(db_session: Session, user_id: int, item_id: int) -> None:
    db_session.query(Cart).filter_by(user_id=user_id, item_id=item_id).delete()
    db_session.commit()
