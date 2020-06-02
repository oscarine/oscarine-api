from typing import Optional

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.db_models.user import User
from app.models.user import UserCreate, UserUpdate


def get_by_email(db_session: Session, *, email: str) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()


def create_user(db_session: Session, *, user_in: UserCreate, otp: int) -> User:
    user = User(
        email=user_in.email, password_hash=get_password_hash(user_in.password), otp=otp
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_by_id(db_session: Session, *, user_id: int) -> Optional[User]:
    user = db_session.query(User).filter(User.id == user_id).first()
    if user:
        return user
    return None


def authenticate(
    db_session: Session, *, email: EmailStr, password: str
) -> Optional[User]:
    user = get_by_email(db_session, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.email_verified:
        raise HTTPException(status_code=401, detail="Email not verified.")
    return user


def update_user_info(db_session: Session, *, user: User, data: UserUpdate) -> User:
    data = jsonable_encoder(data, exclude_none=True)
    if "email" in data:
        user_by_email = get_by_email(db_session, email=data["email"])
        if user_by_email:
            raise HTTPException(
                status_code=422, detail="The user with this email already exists."
            )
    for field in data:
        setattr(user, field, data[field])
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def user_email_verified(db_session: Session, *, user: User) -> User:
    user.email_verified = True
    db_session.commit()
    return user
