from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.error import expected_integrity_error
from app.api.utils.security import get_current_user
from app.crud.item import item_by_ids_and_shop
from app.crud.order import add_ordered_items, create_order
from app.crud.shop import shop_by_id
from app.db_models.user import User
from app.models.order import CreateOrder, OrderDetails

router = APIRouter()


@router.post("/orders", response_model=OrderDetails)
async def create_new_order(
    *,
    db: Session = Depends(get_db),
    data: CreateOrder,
    current_user: User = Depends(get_current_user),
):
    if shop := shop_by_id(db, shop_id=data.shop_id):
        if owner := shop.owner:
            if owner.email_verified:
                ordered_item_ids = [item.item_id for item in data.ordered_items]
                items = item_by_ids_and_shop(
                    db, shop_id=data.shop_id, ids=ordered_item_ids
                )
                if len(items) == len(ordered_item_ids):
                    with expected_integrity_error(
                        db, detail="Error. Cannot create order.", debug=False
                    ):
                        order = create_order(db, data=data, user=current_user)
                        ordered_items = add_ordered_items(
                            db,
                            order=order,
                            ordered_items=data.ordered_items,
                            db_items=items,
                        )
                        return OrderDetails(
                            id=order.id,
                            shop_id=order.shop_id,
                            address_id=order.address_id,
                            user_id=order.user_id,
                            order_datetime=order.order_datetime,
                            user_instructions=order.user_instructions,
                            total_cost=order.total_cost,
                            ordered_items=ordered_items,
                        )
                raise HTTPException(
                    status_code=400, detail="Some item(s) does not exists in this shop."
                )
    raise HTTPException(status_code=400, detail="No such shop exists.")
