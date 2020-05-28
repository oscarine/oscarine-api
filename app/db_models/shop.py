from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relation

from app.db.base_class import Base
from geoalchemy2.types import Geography


class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False)
    phone_number = Column(String(15))
    address = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    owner = relation("Owner", backref='shops')
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    radius_metres = Column(Numeric(asdecimal=True, scale=3), nullable=False)
    items = relation("Item", back_populates="shop")
    orders = relation("Order", back_populates="shop")
