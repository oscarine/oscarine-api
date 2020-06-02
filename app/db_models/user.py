from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), index=True, unique=True, nullable=False)
    password_hash = Column(String(), nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow)
    name = Column(String(30))
    phone_number = Column(String(15))
    avatar_image = Column(String(120))
    email_verified = Column(Boolean, default=False)
    otp = Column(Integer, nullable=False)
    otp_created_at = Column(DateTime, default=datetime.utcnow)
