from typing import Optional
from fastapi.encoders import jsonable_encoder
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


def create_owner(db_session: Session, *, user_in: OwnerCreate) -> Owner:
    owner = Owner(
        username=user_in.username,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password)
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


def authenticate(db_session: Session, *, username: str, password: str) -> Optional[Owner]:
    owner = get_by_username(db_session, username=username)
    if not owner:
        return None
    if not verify_password(password, owner.password_hash):
        return None
    return owner


def update_owner_info(db_session: Session, *, owner: Owner, data: OwnerUpdate) -> Owner:
    owner_data = jsonable_encoder(data)
    data = remove_none_from_dict(owner_data)
    for field in data:
        setattr(owner, field, data[field])
    db_session.add(owner)
    db_session.commit()
    db_session.refresh(owner)
    return owner
