from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db_models.owner import Owner
from app.models.owner import OwnerCreate, OwnerUpdate


def get_by_username(db_session: Session, *, username: str) -> Optional[Owner]:
    return db_session.query(Owner).filter(Owner.username == username).first()


def create_owner(db_session: Session, *, user_in: OwnerCreate, otp: int) -> Owner:
    owner = Owner(
        email=user_in.email, password_hash=get_password_hash(user_in.password), otp=otp
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


def update_owner_info(
    db_session: Session, *, owner: Owner, data: OwnerUpdate, otp: int = None
) -> Owner:
    """If `otp` sent is not None:
    `user.otp = otp`
    `user.email_verified = False`
    `user.otp_created_at = datetime.utcnow()`
    """
    data = jsonable_encoder(data, exclude_none=True)
    for field in data:
        setattr(owner, field, data[field])
    if otp:
        owner.otp = otp
        owner.email_verified = False
        owner.otp_created_at = datetime.utcnow()
    db_session.add(owner)
    db_session.commit()
    db_session.refresh(owner)
    return owner
