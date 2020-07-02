from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.api.utils.calculation import ItemCalculation
from app.api.utils.db import get_db
from app.api.utils.error import expected_integrity_error
from app.api.utils.owner_security import get_current_owner
from app.api.utils.security import get_current_user
from app.crud.address import get_address_by_id
from app.crud.item import item_by_ids_and_shop
from app.crud.order import (
    add_ordered_items,
    create_order,
    edit_order_status,
    get_order_by_id,
)
from app.crud.shop import get_shop_by_id, shop_by_id
from app.db_models.item import Item
from app.db_models.owner import Owner
from app.db_models.user import User
from app.models.order import (
    CreateOrder,
    EditOrderStatusForOwner,
    EditOrderStatusMessage,
    ItemsTotalCost,
    OrderDetails,
    OrderedItem,
    OrderStatusForOwner,
)

router = APIRouter()


@router.post("/orders", response_model=OrderDetails)
async def create_new_order(
    *,
    db: Session = Depends(get_db),
    data: CreateOrder,
    current_user: User = Depends(get_current_user),
):
    if shop := shop_by_id(db, shop_id=data.shop_id):
        if get_address_by_id(db, id=data.address_id, user_id=current_user.id):
            if owner := shop.owner:
                ordered_item_ids = [item.item_id for item in data.ordered_items]
                items = item_by_ids_and_shop(
                    db, shop_id=data.shop_id, ids=ordered_item_ids
                )
                if items and len(items) == len(ordered_item_ids):
                    with expected_integrity_error(
                        db, detail="Error. Cannot create order.", debug=False
                    ):
                        if order := create_order(db, data=data, user=current_user):
                            ordered_items = add_ordered_items(
                                db,
                                order=order,
                                ordered_items=data.ordered_items,
                                db_items=items,
                            )
                            order.ordered_items = ordered_items
                            # TODO: Send order confirmation email to user
                            # and new order email to owner of the shop
                        return order
                raise HTTPException(
                    status_code=400, detail="Some item(s) does not exists in this shop."
                )
        raise HTTPException(status_code=400, detail="Invalid user address.")
    raise HTTPException(status_code=400, detail="No such shop exists.")


@router.put("/orders/{order_id}/status", response_model=EditOrderStatusMessage)
async def edit_order_status_for_owner(
    *,
    order_id: PositiveInt,
    data: EditOrderStatusForOwner,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner),
):
    if order := get_order_by_id(db, id=order_id):
        if shop := get_shop_by_id(db, shop_id=order.shop_id, owner_id=current_owner.id):
            current_status = order.status.code
            if (
                data.status == OrderStatusForOwner.accepted
                or data.status == OrderStatusForOwner.declined
            ):
                if current_status != "pending":
                    raise HTTPException(
                        status_code=400,
                        detail="Only pending order can be accepted or declined.",
                    )
            else:
                if current_status != "accepted":
                    raise HTTPException(
                        status_code=400, detail="Only accepted order can be delivered."
                    )
            if order := edit_order_status(db, order=order, order_status=data.status):
                # TODO: Notify user regarding the new order status through email.
                return EditOrderStatusMessage(
                    status=order.status.value, message="Order status changed."
                )
        raise HTTPException(status_code=403, detail="Not allowed for this owner.")
    raise HTTPException(status_code=404, detail="No such order exists.")


@router.put("/orders/{order_id}/cancel", response_model=EditOrderStatusMessage)
async def cancel_order_for_user(
    *,
    order_id: PositiveInt,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if order := get_order_by_id(db, id=order_id):
        if order.user_id == current_user.id:
            current_status = order.status.code
            if current_status in ["declined", "cancelled", "delivered"]:
                raise HTTPException(status_code=400, detail="Order can't be cancelled.")
            if order := edit_order_status(db, order=order, order_status="cancelled"):
                # TODO: Notify owner that order has been cancelled through email.
                # Also, send email to user that the order has been cancelled.
                return EditOrderStatusMessage(
                    status=order.status.value, message="Order cancelled."
                )
        raise HTTPException(status_code=403, detail="Not allowed for this user.")
    raise HTTPException(status_code=404, detail="No such order exists.")


@router.post("/order-calculation", response_model=ItemsTotalCost)
async def item_calculation(*, db: Session = Depends(get_db), data: List[OrderedItem]):
    item_ids = [item.item_id for item in data]
    items = db.query(Item).filter(Item.id.in_(item_ids)).filter(Item.item_available).all()
    if len(item_ids) == len(items):
        items_cost = ItemCalculation(db, items=data, ids=item_ids)
        return ItemsTotalCost(items_total_cost=items_cost)
    raise HTTPException(status_code=400, detail="One or more item does not exists.")
