from datetime import datetime
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.utils.db import clone_db_model
from app.db_models.address import Address
from app.models.address import EditAddress, UserAddress


def add_user_address(db_session: Session, *, user_id: int, data: UserAddress) -> Address:
    address = Address(user_id=user_id)
    data = jsonable_encoder(data, exclude_none=True)
    for field in data:
        setattr(address, field, data[field])
    address.location = f"POINT({data['longitude']} {data['latitude']})"
    db_session.add(address)
    db_session.commit()
    db_session.refresh(address)
    return address


def get_user_addresses(db_session: Session, *, user_id: int) -> List[Address]:
    addresses = (
        db_session.query(Address)
        .filter(Address.user_id == user_id)
        .order_by(Address.id.desc())
        .all()
    )
    if addresses:
        return addresses
    return None


def get_address_by_id(
    db_session: Session, *, id: int, user_id: int, include_archived: bool = False
) -> Address:
    query = (
        db_session.query(Address)
        .filter(Address.user_id == user_id)
        .filter(Address.id == id)
    )
    if not include_archived:
        query = query.filter(Address.archived == False)
    if address := query.first():
        return address
    return None


def edit_user_address(
    db_session: Session, *, address: Address, data: EditAddress
) -> Address:
    address_clone = clone_db_model(model=address)
    data = jsonable_encoder(data, exclude_none=True)
    for field in data:
        setattr(address_clone, field, data[field])
    if "longitude" in data and "latitude" in data:
        address_clone.location = f"POINT({data['longitude']} {data['latitude']})"
    else:
        address_clone.location = f"POINT({address.longitude} {address.latitude})"
    db_session.add(address_clone)
    # Archive the old address after creating the clone.
    address.archived = True
    db_session.commit()
    db_session.refresh(address_clone)
    return address_clone


def delete_user_address(db_session: Session, *, address: Address):
    address.deleted_at = datetime.utcnow()
    address.archived = True
    db_session.commit()
