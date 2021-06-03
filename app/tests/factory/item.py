from random import randint
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.choices.cost_unit import COST_UNIT_TYPES
from app.db_models.item import Item
from app.tests.factory.base import Base


class ItemFactory(Base):
    def __init__(self, shop_id: int, owner_id: int) -> None:
        self.name = self.random_lower_string()
        self.cost = self.random_integer()
        self.cost_unit = COST_UNIT_TYPES[randint(0, len(COST_UNIT_TYPES) - 1)][0]
        self.shop_id = shop_id
        self.owner_id = owner_id

    def create(self, db: Session):
        item = Item(
            name=self.name,
            cost=self.cost,
            cost_unit=self.cost_unit,
            shop_id=self.shop_id,
            owner_id=self.owner_id,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        self.id = item.id
        self.item_available = item.item_available

    def update(self, db: Session, values: Dict[str, Any]):
        item: Item = db.query(Item).filter_by(id=self.id).first()
        for key in values:
            setattr(item, key, values[key])
        db.add(item)
        db.commit()
        db.refresh(item)
        for key in values:
            setattr(self, key, getattr(item, key))
