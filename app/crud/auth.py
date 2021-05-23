from typing import Optional

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.db_models.owner import Owner
from app.db_models.user import User


def get_owner_by_email(db_session: Session, *, email: str) -> Optional[Owner]:
    return db_session.query(Owner).filter(Owner.email == email).first()


def get_user_by_email(db_session: Session, *, email: str) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()


def owner_authenticate(
    db_session: Session, *, email: EmailStr, password: str
) -> Optional[Owner]:
    owner = get_owner_by_email(db_session, email=email)
    if not owner:
        return None
    if not verify_password(password, owner.password_hash):
        return None
    if not owner.email_verified:
        raise HTTPException(status_code=401, detail="Email not verified.")
    return owner


def user_authenticate(
    db_session: Session, *, email: EmailStr, password: str
) -> Optional[User]:
    user = get_user_by_email(db_session, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def owner_email_verified(db_session: Session, *, owner: Owner) -> Owner:
    owner.email_verified = True
    db_session.commit()
    return owner


def user_email_verified(db_session: Session, *, user: User) -> User:
    user.email_verified = True
    db_session.commit()
    return user
