from typing import List, Tuple

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.db_models.cart import Cart
from app.db_models.item import Item
from app.models.cart import (
    CartItemDetail,
    CartUpdateChoiceEnum,
    UpdateCartItem,
    ViewCartResponse,
)


def add_cart_item(db_session: Session, user_id: int, shop_id: str, item_id: int):
    cart_item = Cart(item_id=item_id, user_id=user_id, shop_id=shop_id)
    db_session.add(cart_item)
    db_session.commit()


def get_cart_item(db_session: Session, user_id: int, item_id: int) -> Cart:
    return db_session.query(Cart).filter_by(user_id=user_id, item_id=item_id).first()


def update_cart_item(db_session: Session, cart_item: Cart, data: UpdateCartItem):
    if data.action == CartUpdateChoiceEnum.minus and cart_item.item_quantity > 1:
        cart_item.item_quantity = cart_item.item_quantity - 1
    elif data.action == CartUpdateChoiceEnum.plus:
        cart_item.item_quantity = cart_item.item_quantity + 1
    else:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
    db_session.add(cart_item)
    db_session.commit()


def get_cart_items_detailed(db_session: Session, user_id: int) -> ViewCartResponse:
    cart_info: List[Tuple[Cart, Item]] = (
        db_session.query(Cart, Item).filter(Cart.user_id == user_id).join(Item).all()
    )
    total_items: int = 0
    total_cost: float = 0
    unique_items: int = len(cart_info)
    items: List[CartItemDetail] = []
    if unique_items <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EMPTY_CART")
    for cart_item in cart_info:
        cart, item = cart_item
        total_items += cart.item_quantity
        total_cost += cart.item_quantity * item.cost
        items.append(
            CartItemDetail(
                id=item.id,
                name=item.name,
                cost=item.cost,
                item_quantity=cart.item_quantity,
                item_available=item.item_available,
            )
        )
    return ViewCartResponse(
        total_items=total_items,
        unique_items=unique_items,
        total_cost=total_cost,
        items=items,
    )


def delete_cart_item(db_session: Session, user_id: int, item_id: int) -> None:
    db_session.query(Cart).filter_by(user_id=user_id, item_id=item_id).delete()
    db_session.commit()


def empty_cart(db_session: Session, user_id: int) -> int:
    unique_items_count = (
        db_session.query(Cart)
        .filter_by(user_id=user_id)
        .delete(synchronize_session=False)
    )
    db_session.commit()
    return unique_items_count
