from sqlalchemy import Column, String, Integer

from app.db.base_class import Base


class Owner(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String())
    first_name = Column(String(25))
    last_name = Column(String(25))
    phone_number = Column(String(15))
    avatar_image = Column(String(120))
    city = Column(String(30))
    state = Column(String(30))
