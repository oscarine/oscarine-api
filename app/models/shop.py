from typing import Optional

from pydantic import (
    BaseModel,
    PositiveFloat,
    StrictBool,
    confloat,
    constr,
    root_validator,
)


class ShopDetails(BaseModel):
    id: str
    name: str
    address: str
    owner_id: int
    radius_metres: float
    phone_number: Optional[str]
    is_available: bool

    class Config:
        orm_mode = True


class ShopViewForUser(BaseModel):
    id: int
    name: str
    address: str
    radius_metres: float
    is_available: bool
    deliverable: Optional[bool] = None

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


class ShopUpdate(BaseModel):
    name: Optional[constr(min_length=3, max_length=50)]
    phone_number: Optional[constr(min_length=10, max_length=15)]
    address: Optional[constr(min_length=5, max_length=50)]
    longitude: Optional[confloat(gt=-180, lt=180)]
    latitude: Optional[confloat(gt=-90, lt=90)]
    radius_metres: Optional[PositiveFloat]
    is_available: Optional[StrictBool]

    @root_validator(pre=True)
    def longitude_latitude_or_neither(cls, values):
        """Both longitude and latitude should be
        provided or neither of them should be provided.
        """
        longitude, latitude = values.get("longitude"), values.get("latitude")
        if longitude is not None and latitude is not None:
            return values
        elif longitude is None and latitude is None:
            return values
        raise ValueError(
            "Both longitude and latitude should be provided or neither of them."
        )
