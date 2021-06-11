from sqlalchemy.orm import Session

from app.db_models.address import Address
from app.tests.factory.base import Base


class AddressFactory(Base):
    def __init__(self, user_id: int, longitude: float, latitude: float) -> None:
        self.id = None
        self.user_id = user_id
        self.longitude = longitude
        self.latitude = latitude
        self.complete_address = self.random_lower_string()
        self.tag = self.random_lower_string(str_length=15)

    def create(self, db: Session) -> None:
        address = Address(
            user_id=self.user_id,
            longitude=self.longitude,
            latitude=self.latitude,
            complete_address=self.complete_address,
            location=f"POINT({self.longitude} {self.latitude})",
            tag=self.tag,
        )
        db.add(address)
        db.commit()
        db.refresh(address)
        self.id = address.id
