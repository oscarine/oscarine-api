from pydantic import BaseModel, constr, confloat, PositiveFloat
from typing import Optional


class ShopDetails(BaseModel):
    id: int
    name: str
    address: str
    owner_id: int
    radius_metres: float
    phone_number: Optional[str]

    class Config:
        orm_mode = True


class ShopDetailsForUsers(BaseModel):
    id: int
    name: str
    address: str
    phone_number: Optional[str]

    class Config:
        orm_mode = True


class ShopRegister(BaseModel):
    name: constr(min_length=3, max_length=50)
    longitude: confloat(gt=-180, lt=180)
    latitude: confloat(gt=-90, lt=90)
    address: constr(min_length=5, max_length=50)
    radius_metres: PositiveFloat
    phone_number: Optional[constr(min_length=10, max_length=15)]
