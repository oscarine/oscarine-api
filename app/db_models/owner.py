from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime

from app.db.base_class import Base


class Owner(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String())
    name = Column(String(30))
    phone_number = Column(String(15))
    avatar_image = Column(String(120))
    last_seen = Column(DateTime, default=datetime.utcnow)
    city = Column(String(30))
    state = Column(String(30))
    email_verified = Column(Boolean, default=False)
    otp = Column(Integer, nullable=False)
