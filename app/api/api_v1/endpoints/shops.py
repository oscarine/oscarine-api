from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import PositiveInt, confloat
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.owner_security import get_current_owner
from app.api.utils.pagination import pagination
from app.api.utils.security import get_current_user
from app.crud.shop import get_shop_by_id, register_new_shop, shops_for_users, update_shop
from app.db_models.owner import Owner as DBOwnerModel
from app.db_models.user import User as DBUser
from app.models.shop import ShopDetails, ShopDetailsForUsers, ShopRegister, ShopUpdate

router = APIRouter()


@router.post("/shops", response_model=ShopDetails, status_code=201)
async def register_shop(
    *,
    db: Session = Depends(get_db),
    data: ShopRegister,
    current_owner: DBOwnerModel = Depends(get_current_owner),
    response: Response,
):
    shop = register_new_shop(db, owner_id=current_owner.id, data=data)
    response.status_code = status.HTTP_201_CREATED
    return shop


@router.get("/shops", response_model=List[ShopDetails])
async def list_of_shops(
    *,
    db: Session = Depends(get_db),
    current_owner: DBOwnerModel = Depends(get_current_owner),
):
    if (shops := current_owner.shops) :
        return shops
    raise HTTPException(status_code=404, detail="This owner does not have any shops.")


@router.get("/shops/{shop_id}", response_model=ShopDetails)
async def shop_by_id(
    *,
    shop_id: PositiveInt,
    db: Session = Depends(get_db),
    current_owner: DBOwnerModel = Depends(get_current_owner),
):
    shop = get_shop_by_id(db, shop_id=shop_id, owner_id=current_owner.id)
    if shop:
        return shop
    raise HTTPException(
        status_code=404, detail="This owner does not have any shop with this id."
    )


@router.get("/shops-list", response_model=List[ShopDetailsForUsers])
async def list_of_shops_for_users(
    *,
    longitude: confloat(gt=-180, lt=180),
    latitude: confloat(gt=-90, lt=90),
    page: PositiveInt = 1,
    page_size: PositiveInt = 10,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    shops = shops_for_users(db, longitude=longitude, latitude=latitude)
    shops = pagination(query=shops, page_number=page, page_size=page_size).all()
    if shops:
        return shops
    raise HTTPException(status_code=404, detail="Cannot find shops for your location.")


@router.patch("/shops/{shop_id}", response_model=ShopDetails)
async def owner_update_shop(
    *,
    shop_id: PositiveInt,
    db: Session = Depends(get_db),
    data: ShopUpdate,
    current_owner: DBOwnerModel = Depends(get_current_owner),
):
    if shop := get_shop_by_id(db, shop_id=shop_id, owner_id=current_owner.id):
        if shop := update_shop(db, shop=shop, data=data):
            return shop
    raise HTTPException(status_code=403, detail="This owner cannot update this shop.")
