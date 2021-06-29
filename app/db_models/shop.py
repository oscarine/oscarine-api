from random import randint

from geoalchemy2.types import Geography
from slugify import slugify
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, event
from sqlalchemy.orm import relation

from app.db.base_class import Base


class Shop(Base):
    __tablename__ = 'shops'

    id = Column(String(length=100), primary_key=True, index=True)
    name = Column(String(length=50), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    phone_number = Column(String(15))
    address = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    owner = relation("Owner", backref='shops')
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    radius_metres = Column(Numeric(asdecimal=True, scale=3), nullable=False)
    items = relation("Item", back_populates="shop")

    @staticmethod
    def slugify_id(target, value: str, oldvalue: str, _):
        if value and (not target.id or value != oldvalue):
            value = value + " " + str(randint(100000, 999999))
            target.id = slugify(value, max_length=100)


event.listen(Shop.name, "set", Shop.slugify_id, retval=False)
