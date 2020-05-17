from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt, confloat
from typing import List

from sqlalchemy.orm import Session
from app.api.utils.db import get_db
from app.db_models.owner import Owner as DBOwnerModel
from app.api.utils.owner_security import get_current_owner
from app.models.shop import ShopDetails, ShopRegister, ShopDetailsForUsers
from app.crud.shop import register_new_shop, get_shop_by_id, shops_for_users
from app.api.utils.security import get_current_user
from app.db_models.user import User as DBUser


router = APIRouter()


@router.post("/shops", response_model=ShopDetails)
async def register_shop(
    *,
    db: Session = Depends(get_db),
    data: ShopRegister,
    current_owner: DBOwnerModel = Depends(get_current_owner)
):
    shop = register_new_shop(db, owner_id=current_owner.id, data=data)
    return shop


@router.get("/shops", response_model=List[ShopDetails])
async def list_of_shops(
    *,
    db: Session = Depends(get_db),
    current_owner: DBOwnerModel = Depends(get_current_owner)
):
    if (shops := current_owner.shops):
        return shops
    raise HTTPException(
        status_code=404,
        detail="This owner does not have any shops."
    )


@router.get("/shops/{shop_id}", response_model=ShopDetails)
async def shop_by_id(
    *,
    shop_id: PositiveInt,
    db: Session = Depends(get_db),
    current_owner: DBOwnerModel = Depends(get_current_owner)
):
    shop = get_shop_by_id(db, shop_id=shop_id, owner_id=current_owner.id)
    if shop:
        return shop
    raise HTTPException(
        status_code=404,
        detail="This owner does not have any shop with this id."
    )


@router.get("/shops-list", response_model=List[ShopDetailsForUsers])
async def list_of_shops_for_users(
    *,
    longitude: confloat(gt=-180, lt=180),
    latitude: confloat(gt=-90, lt=90),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    shops = shops_for_users(db, longitude=longitude, latitude=latitude)
    if shops:
        return shops
    raise HTTPException(
        status_code=404,
        detail="Cannot find shops for your location."
    )
