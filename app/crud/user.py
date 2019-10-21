from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.db_models.user import User
from app.models.user import UserCreate


def get_by_username(db_session: Session, *, username: str) -> Optional[User]:
    return db_session.query(User).filter(User.username == username).first()


def get_by_email(db_session: Session, *, email: str) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()


def create_user(db_session: Session, *, user_in: UserCreate) -> User:
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password)
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    del user.password_hash  # dont send hashed password in response
    return user


def get_by_id(db_session: Session, *, user_id: int) -> Optional[User]:
    user = db_session.query(User).filter(User.id == user_id).first()
    if user:
        del user.password_hash  # dont send hashed password in response
        return user
    return None
