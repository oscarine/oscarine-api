from sqlalchemy import Column, String, Integer, DateTime, Boolean

from app.db.base_class import Base
from datetime import datetime


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String())
    last_seen = Column(DateTime, default=datetime.utcnow)
    name = Column(String(30))
    phone_number = Column(String(15))
    avatar_image = Column(String(120))
    email_verified = Column(Boolean, default=False)
    otp = Column(Integer, nullable=False)
    otp_created_at = Column(DateTime, default=datetime.utcnow)
