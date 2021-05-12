from geoalchemy2.types import Geography
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relation

from app.db.base_class import Base


class Address(Base):
    """To store the addresses of user.

    `tag` can be Home, Work, Other etc.
    """

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relation("User", backref='addresses')
    longitude = Column(Numeric(precision=15, scale=10), nullable=False)
    latitude = Column(Numeric(precision=15, scale=10), nullable=False)
    complete_address = Column(String(length=300), nullable=False)
    location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    tag = Column(String(length=30), nullable=False)
    floor = Column(String(length=50))
    landmark = Column(String(length=100))

    # Immutable address
    deleted_at = Column(DateTime)
    archived = Column(Boolean, default=False)
