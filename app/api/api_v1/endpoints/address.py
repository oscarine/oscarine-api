from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.crud.address import (
    add_user_address,
    delete_user_address,
    edit_user_address,
    get_address_by_id,
    get_user_addresses,
)
from app.db_models.user import User
from app.models.address import (
    AddressDetails,
    DeleteAddressResponse,
    EditAddress,
    UserAddress,
)

router = APIRouter()


@router.post("/addresses", response_model=AddressDetails)
async def add_new_address(
    *,
    db: Session = Depends(get_db),
    data: UserAddress,
    current_user: User = Depends(get_current_user),
):
    if new_address := add_user_address(db, user_id=current_user.id, data=data):
        return new_address
    raise HTTPException(status_code=400, detail="Cannot add new address.")


@router.get("/addresses", response_model=List[AddressDetails])
async def list_of_addresses(
    *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),
):
    if addresses := get_user_addresses(db, user_id=current_user.id):
        return addresses
    raise HTTPException(status_code=404, detail="This user does not have any address.")


@router.get("/addresses/{address_id}", response_model=AddressDetails)
async def single_address(
    *,
    address_id: PositiveInt,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if address := get_address_by_id(db, id=address_id, user_id=current_user.id):
        return address
    raise HTTPException(
        status_code=404, detail="This user does not have any address with this id."
    )


@router.patch("/addresses/{address_id}", response_model=AddressDetails)
async def edit_address(
    *,
    address_id: PositiveInt,
    data: EditAddress,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if address := get_address_by_id(db, id=address_id, user_id=current_user.id):
        if address := edit_user_address(db, address=address, data=data):
            return address
    raise HTTPException(
        status_code=401, detail="This user cannot edit address with this id."
    )


@router.delete("/addresses/{address_id}", response_model=DeleteAddressResponse)
async def delete_address(
    *,
    address_id: PositiveInt,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if address := get_address_by_id(db, id=address_id, user_id=current_user.id):
        delete_user_address(db, address=address)
        return DeleteAddressResponse(message="Address deleted successfully.")
    raise HTTPException(
        status_code=401, detail="This user cannot delete address with this id."
    )
