from typing import List, Optional

from pydantic import BaseModel, PositiveInt, constr


class OrderedItem(BaseModel):
    item_id: PositiveInt
    quantity: PositiveInt


class CreateOrder(BaseModel):
    shop_id: PositiveInt
    user_instructions: Optional[constr(min_length=1, max_length=150)]
    ordered_items: List[OrderedItem]
