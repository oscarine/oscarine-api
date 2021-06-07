from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.owner_security import get_current_owner
from app.api.utils.parsing import convert_cost_units
from app.crud.item import (
    add_item,
    item_by_id_and_owner,
    item_by_name_and_shop,
    items_by_shop_id,
    update_item,
)
from app.crud.shop import get_shop_by_id
from app.db_models.owner import Owner
from app.models.item import Item, ItemResponseForOwner, ItemResponseForUser, UpdateItem

router = APIRouter()


@router.post("/items/{shop_id}", response_model=ItemResponseForOwner, status_code=201)
async def add_item_to_shop(
    *,
    shop_id: PositiveInt,
    db: Session = Depends(get_db),
    data: Item,
    current_owner: Owner = Depends(get_current_owner),
):
    if get_shop_by_id(db, shop_id=shop_id, owner_id=current_owner.id):
        if item_by_name_and_shop(db, shop_id=shop_id, name=data.name):
            # Item name not unique within the shop. Show exception.
            raise HTTPException(
                status_code=409, detail="Item with this name already exists."
            )
        return add_item(db, shop_id=shop_id, owner_id=current_owner.id, data=data)
    raise HTTPException(
        status_code=403, detail="This owner is not allowed to add items to this shop."
    )


@router.patch("/items/{item_id}")
async def edit_item(
    *,
    item_id: PositiveInt,
    data: UpdateItem,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner),
):
    if item := item_by_id_and_owner(db, item_id=item_id, owner_id=current_owner.id):
        if item_name := data.name:
            # Owner wants to update the name of the item.
            if item_by_name_and_shop(db, shop_id=item.shop_id, name=item_name):
                # Item name not unique within the shop. Show exception.
                raise HTTPException(
                    status_code=409, detail="Item with this name already exists."
                )
        return update_item(db, item=item, data=data)
    raise HTTPException(
        status_code=403, detail="This owner is not allowed to edit this item."
    )


@router.get("/items/{shop_id}", response_model=List[ItemResponseForOwner])
async def get_items_for_owner(
    *,
    shop_id: PositiveInt,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner),
):
    shop = get_shop_by_id(db, shop_id=shop_id, owner_id=current_owner.id)
    if shop:
        if items := shop.items:
            return convert_cost_units(items)
        raise HTTPException(
            status_code=404, detail="This shop does not have any items."
        )
    raise HTTPException(
        status_code=403, detail="This owner is not allowed to view items of this shop."
    )


@router.get("/items-list/{shop_id}", response_model=List[ItemResponseForUser])
async def get_items_for_user(
    *,
    shop_id: PositiveInt,
    db: Session = Depends(get_db),
):
    if items := items_by_shop_id(db, shop_id=shop_id):
        return convert_cost_units(items)
    raise HTTPException(status_code=404, detail="This shop does not have any items.")
