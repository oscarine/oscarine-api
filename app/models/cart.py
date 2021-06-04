from enum import Enum
from typing import List

from pydantic import BaseModel, PositiveInt


class CartResponse(BaseModel):
    item_id: int
    item_quantity: int

    class Config:
        orm_mode = True


class CartItem(BaseModel):
    item_id: PositiveInt


class CartUpdateChoiceEnum(str, Enum):
    plus = 'plus'
    minus = 'minus'


class UpdateCartItem(CartItem):
    action: CartUpdateChoiceEnum


# = Field(int, alias='item_id')
class CartItemDetail(BaseModel):
    id: int
    name: str
    cost: float
    item_quantity: int
    item_available: bool


class ViewCartResponse(BaseModel):
    total_items: int
    unique_items: int
    total_cost: float
    items: List[CartItemDetail]


class DeleteCartItemResponse(BaseModel):
    message: str
