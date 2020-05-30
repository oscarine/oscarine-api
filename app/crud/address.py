from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

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


def get_address_by_id(db_session: Session, *, id: int, user_id: int) -> Address:
    address = (
        db_session.query(Address)
        .filter(Address.user_id == user_id)
        .filter(Address.id == id)
        .first()
    )
    if address:
        return address
    return None


def edit_user_address(
    db_session: Session, *, address: Address, data: EditAddress
) -> Address:
    data = jsonable_encoder(data, exclude_none=True)
    for field in data:
        setattr(address, field, data[field])
    if "longitude" in data and "latitude" in data:
        address.location = f"POINT({data['longitude']} {data['latitude']})"
    db_session.commit()
    db_session.refresh(address)
    return address


def delete_user_address(db_session: Session, *, address: Address):
    db_session.delete(address)
    db_session.commit()
