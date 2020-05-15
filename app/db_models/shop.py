from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relation
from geoalchemy2.types import Geography

from app.db.base_class import Base


class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False)
    phone_number = Column(String(15))
    address = Column(String(50))
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    owner = relation("Owner", backref='shops')
    location = Column(Geography(geometry_type='POINT', srid=4326))
    