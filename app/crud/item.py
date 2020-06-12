from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db_models.item import Item
from app.models.item import Item as PydanticItem
from app.models.item import UpdateItem


def item_by_name_and_shop(db_session: Session, *, shop_id: int, name: str) -> Item:
    item = db_session.query(Item).filter_by(shop_id=shop_id, name=name).first()
    if item:
        return item
    return None


def add_item(
    db_session: Session, *, shop_id: int, owner_id: int, data: PydanticItem
) -> Item:
    item = Item()
    data = jsonable_encoder(data, exclude_none=True)
    for field in data:
        setattr(item, field, data[field])
    item.shop_id = shop_id
    item.owner_id = owner_id
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    item.cost_unit = item.cost_unit.value
    return item


def item_by_id_and_owner(db_session: Session, *, item_id: int, owner_id: int) -> Item:
    item = db_session.query(Item).filter_by(id=item_id, owner_id=owner_id).first()
    if item:
        return item
    return None


def update_item(db_session: Session, *, item: Item, data: UpdateItem) -> Item:
    data = jsonable_encoder(data, exclude_none=True)
    for field in data:
        setattr(item, field, data[field])
    db_session.commit()
    db_session.refresh(item)
    item.cost_unit = item.cost_unit.value
    return item


def items_by_shop_id(db_session: Session, *, shop_id: int) -> List[Item]:
    items = db_session.query(Item).filter_by(shop_id=shop_id).all()
    if items:
        return items
    return None


def item_by_ids_and_shop(
    db_session: Session, *, shop_id: int, ids: List[int]
) -> List[Item]:
    items = (
        db_session.query(Item)
        .filter(Item.id.in_(ids))
        .filter(Item.shop_id == shop_id)
        .filter(Item.item_available)
        .all()
    )
    if items:
        return items
    return None
