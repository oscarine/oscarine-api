from typing import Optional
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.db_models.owner import Owner
from app.models.owner import OwnerCreate, OwnerUpdate
from app.core.security import get_password_hash, verify_password
from app.api.utils.parsing import remove_none_from_dict


def get_by_username(db_session: Session, *, username: str) -> Optional[Owner]:
    return db_session.query(Owner).filter(Owner.username == username).first()


def get_by_email(db_session: Session, *, email: str) -> Optional[Owner]:
    return db_session.query(Owner).filter(Owner.email == email).first()


def create_owner(db_session: Session, *, user_in: OwnerCreate,
                 otp: int) -> Owner:
    owner = Owner(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        otp=otp
    )
    db_session.add(owner)
    db_session.commit()
    db_session.refresh(owner)
    return owner


def get_by_id(db_session: Session, *, owner_id: int) -> Optional[Owner]:
    owner = db_session.query(Owner).filter(Owner.id == owner_id).first()
    if owner:
        return owner
    return None


def authenticate(db_session: Session, *, email: EmailStr,
                 password: str) -> Optional[Owner]:
    owner = get_by_email(db_session, email=email)
    if not owner:
        return None
    if not verify_password(password, owner.password_hash):
        return None
    if not owner.email_verified:
        raise HTTPException(
            status_code=401,
            detail="Email not verified."
        )
    return owner


def update_owner_info(db_session: Session, *, owner: Owner,
                      data: OwnerUpdate) -> Owner:
    owner_data = jsonable_encoder(data)
    data = remove_none_from_dict(owner_data)
    if "email" in data:
        owner_by_email = get_by_email(db_session, email=data["email"])
        if owner_by_email:
            raise HTTPException(
                status_code=422,
                detail="The owner with this email already exists."
            )
    for field in data:
        setattr(owner, field, data[field])
    db_session.add(owner)
    db_session.commit()
    db_session.refresh(owner)
    return owner


def owner_email_verified(db_session: Session, *, owner: Owner) -> Owner:
    owner.email_verified = True
    db_session.commit()
    return owner
