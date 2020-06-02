from typing import List

from sqlalchemy.orm import Session

from app.db_models.item import Item
from app.db_models.order import Order
from app.db_models.ordered_item import OrderedItem as OrderedItemDbModel
from app.db_models.user import User
from app.models.order import CreateOrder, OrderedItem


def create_order(db_session: Session, *, data: CreateOrder, user: User) -> Order:
    order = Order(user_id=user.id, shop_id=data.shop_id, address_id=data.address_id)
    if data.user_instructions:
        order.user_instructions = data.user_instructions
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order


def add_ordered_items(
    db_session: Session,
    *,
    order: Order,
    ordered_items: List[OrderedItem],
    db_items: List[Item],
) -> List[OrderedItemDbModel]:
    items = []
    for item in ordered_items:
        for db_item in db_items:
            if db_item.id is item.item_id:
                ordered_item = OrderedItemDbModel(
                    order_id=order.id,
                    item_id=item.item_id,
                    quantity=item.quantity,
                    cost=db_item.cost,
                )
                items.append(ordered_item)
    db_session.add_all(items)
    db_session.commit()
    return items
