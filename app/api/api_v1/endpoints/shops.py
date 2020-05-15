from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from app.api.utils.db import get_db
from app.db_models.owner import Owner as DBOwnerModel
from app.api.utils.owner_security import get_current_owner
from app.models.shop import ShopDetails, ShopRegister
from app.crud.shop import register_new_shop


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
