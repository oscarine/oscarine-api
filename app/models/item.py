from enum import Enum
from typing import Optional

from pydantic import BaseModel, PositiveFloat, StrictBool, constr


class CostUnitEnum(str, Enum):
    per_piece = 'per-piece'
    per_packet = 'per-packet'
    per_unit = 'per-unit'
    per_pack = 'per-pack'
    per_crate = 'per-crate'
    per_kg = 'per-kg'
    per_litre = 'per-litre'


class Item(BaseModel):
    name: constr(min_length=1, max_length=40)
    cost: PositiveFloat
    cost_unit: CostUnitEnum
    category: constr(min_length=1, max_length=25)
    item_available: Optional[StrictBool] = True

    class Config:
        orm_mode = True


class ItemResponseForOwner(BaseModel):
    id: int
    name: str
    cost: float
    cost_unit: str
    category: str
    item_available: bool
    order_count: int
    shop_id: str
    owner_id: int

    class Config:
        orm_mode = True


class ItemResponseForUser(BaseModel):
    id: int
    name: str
    cost: float
    cost_unit: str
    category: Optional[str] = None
    item_available: bool

    class Config:
        orm_mode = True


class UpdateItem(BaseModel):
    name: Optional[constr(min_length=1, max_length=40)]
    cost: Optional[PositiveFloat]
    cost_unit: Optional[CostUnitEnum]
    category: Optional[constr(min_length=1, max_length=25)]
    item_available: Optional[StrictBool]

    class Config:
        orm_mode = True
