from typing import Any, Dict

from sqlalchemy.orm.session import Session

from app.db_models.shop import Shop
from app.tests.factory.base import Base


class ShopFactory(Base):
    def __init__(
        self, longitude: float, latitude: float, owner_id: int, radius_metres: int
    ) -> None:
        self.longitude = longitude
        self.latitude = latitude
        self.name = self.random_lower_string()
        self.address = self.random_lower_string()
        self.owner_id = owner_id
        self.radius_metres = radius_metres

    def create(self, db: Session) -> None:
        shop = Shop(
            name=self.name,
            address=self.address,
            owner_id=self.owner_id,
            radius_metres=self.radius_metres,
            location=f'POINT({self.longitude} {self.latitude})',
        )
        db.add(shop)
        db.commit()
        db.refresh(shop)
        self.id = shop.id

    def update(self, db: Session, values: Dict[str, Any]) -> None:
        shop: Shop = db.query(Shop).filter_by(id=self.id).first()
        for key in values:
            setattr(shop, key, values[key])
        db.add(shop)
        db.commit()
        db.refresh(shop)
        for key in values:
            setattr(self, key, getattr(shop, key))
