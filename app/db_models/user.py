from sqlalchemy import Column, String, Integer, DateTime

from app.db.base_class import Base
from datetime import datetime


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String())
    bio = Column(String(140))
    last_seen = Column(DateTime, default=datetime.utcnow)
    first_name = Column(String(25))
    last_name = Column(String(25))
    phone_number = Column(String(15))
    avatar_image = Column(String(120))
    city = Column(String(30))
    state = Column(String(30))
    role = Column(String(10), default="customer")
