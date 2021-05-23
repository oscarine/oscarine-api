from sqlalchemy.orm import Session

from app.api.utils.otp import generate_random_otp
from app.crud.owner import create_owner as crud_create_owner
from app.models.owner import OwnerCreate
from app.tests.utils.utils import random_email, random_lower_string


def create_owner(*, db: Session, with_verified_email: bool = True):
    email = random_email()
    password = random_lower_string()
    owner_data = OwnerCreate(email=email, password=password)
    otp = generate_random_otp()
    owner = crud_create_owner(db, user_in=owner_data, otp=otp)
    if with_verified_email:
        owner.email_verified = True
        db.add(owner)
        db.commit()
        db.refresh(owner)
    return owner
