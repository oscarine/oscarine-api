from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic.types import PositiveInt
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.error import expected_integrity_error
from app.api.utils.security import get_current_user
from app.crud.cart import (
    add_cart_item,
    delete_cart_item,
    empty_cart,
    get_cart_item,
    get_cart_items_detailed,
    update_cart_item,
)
from app.crud.item import get_available_item
from app.db_models.user import User
from app.models.cart import (
    CartItem,
    CartUpdateChoiceEnum,
    DeleteCartResponse,
    UpdateCartItem,
    ViewCartResponse,
)

router = APIRouter()


@router.post("/cart", response_model=ViewCartResponse, status_code=201)
async def add_item_in_cart(
    *,
    db: Session = Depends(get_db),
    data: CartItem,
    current_user: User = Depends(get_current_user),
):
    """Authenticated user can add items to his/her cart
    and each item added should be from the same shop.

    Status code = 400 and error detail tag = `CONSTRAINT_VIOLATION`.
        Error will occur when a user tries to add item which already exist
        or when the item is from a different shop as compared to the items
        which already exist in the cart.

    Status code = 400 and error detail tag = `NOT_AVAILABLE`.
        Error will occur when the item or the concerned shop is not available.
    """

    if shop_and_item := get_available_item(db, item_id=data.item_id):
        item, shop = shop_and_item
        with expected_integrity_error(
            db,
            detail="CONSTRAINT_VIOLATION: Item already exist in your cart or you are trying to add item from different shops",
            status_code=status.HTTP_400_BAD_REQUEST,
            debug=False,
        ):
            add_cart_item(db, user_id=current_user.id, shop_id=shop.id, item_id=item.id)
            cart_info: ViewCartResponse = get_cart_items_detailed(
                db, user_id=current_user.id
            )
            return cart_info
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="NOT_AVAILABLE: Shop or item not available currently",
    )


@router.patch("/cart", response_model=ViewCartResponse, status_code=200)
async def update_item_in_cart(
    *,
    db: Session = Depends(get_db),
    data: UpdateCartItem,
    current_user: User = Depends(get_current_user),
):
    if item := get_cart_item(db, user_id=current_user.id, item_id=data.item_id):
        if item.item_quantity <= 1 and data.action == CartUpdateChoiceEnum.minus:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="INVALID_ACTION: Item quantity cannot be less than unity",
            )
        update_cart_item(db, cart_item=item, data=data)
        cart_info: ViewCartResponse = get_cart_items_detailed(
            db, user_id=current_user.id
        )
        return cart_info
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="INVALID_ITEM: No such cart item for this user",
    )


@router.get("/cart", response_model=ViewCartResponse, status_code=200)
async def view_cart(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_info: ViewCartResponse = get_cart_items_detailed(db, user_id=current_user.id)
    return cart_info


@router.delete("/cart/{item_id}", response_model=ViewCartResponse, status_code=200)
async def delete_item_from_cart(
    *,
    item_id: PositiveInt,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_cart_item(db, user_id=current_user.id, item_id=item_id)
    cart_info: ViewCartResponse = get_cart_items_detailed(db, user_id=current_user.id)
    return cart_info


@router.delete("/cart", response_model=DeleteCartResponse, status_code=200)
async def empty_current_cart(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    For deleting all the items from cart.
    """
    count = empty_cart(db, user_id=current_user.id)
    return DeleteCartResponse(
        message=f"DELETED: {count} unique items removed from cart"
    )
