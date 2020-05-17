from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from typing import List

from sqlalchemy.orm import Session
from app.api.utils.db import get_db
from app.db_models.owner import Owner as DBOwnerModel
from app.api.utils.owner_security import get_current_owner
from app.models.shop import ShopDetails, ShopRegister
from app.crud.shop import register_new_shop, get_shop_by_id


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
