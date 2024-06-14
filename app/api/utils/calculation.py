from typing import List

from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.db_models.item import Item
from app.models.order import OrderedItem


def ItemCalculation(
    db_session: Session, *, items: List[OrderedItem], ids: List[PositiveInt]
):
    items_cost = 0
    item_id_cost = db_session.query(Item.id, Item.cost).filter(Item.id.in_(ids)).all()
    for i in range(0, len(item_id_cost)):
        for each_item in items:
            if item_id_cost[i][0] == each_item.item_id:
                items_cost = items_cost + (each_item.quantity * item_id_cost[i][1])

    db_session.commit()
    return items_cost
