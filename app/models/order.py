from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, PositiveInt, constr


class OrderedItem(BaseModel):
    item_id: PositiveInt
    quantity: PositiveInt


class CreateOrder(BaseModel):
    shop_id: constr(to_lower=True, min_length=8, max_length=100)
    address_id: PositiveInt
    user_instructions: Optional[constr(min_length=1, max_length=150)]
    ordered_items: List[OrderedItem]


class OrderedItemDetails(BaseModel):
    item_id: int
    quantity: int
    cost: float

    class Config:
        orm_mode = True


class OrderDetails(BaseModel):
    id: int
    shop_id: str
    address_id: int
    user_id: int
    order_datetime: datetime
    user_instructions: Optional[str]
    total_cost: float
    ordered_items: List[OrderedItemDetails]

    class Config:
        orm_mode = True


class OrderStatusForOwner(str, Enum):
    accepted = 'accepted'
    declined = 'declined'
    delivered = 'delivered'


class EditOrderStatusForOwner(BaseModel):
    status: OrderStatusForOwner


class EditOrderStatusMessage(BaseModel):
    status: str
    message: str
