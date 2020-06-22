from typing import Optional

from pydantic import BaseModel, confloat, constr, root_validator


class UserAddress(BaseModel):
    longitude: confloat(gt=-180, lt=180)
    latitude: confloat(gt=-90, lt=90)
    complete_address: constr(min_length=5, max_length=300)
    tag: constr(min_length=1, max_length=30)
    floor: Optional[constr(min_length=1, max_length=50)]
    landmark: Optional[constr(min_length=1, max_length=100)]


class AddressDetails(BaseModel):
    id: int
    user_id: int
    longitude: float
    latitude: float
    complete_address: str
    tag: str
    floor: Optional[str]
    landmark: Optional[str]

    class Config:
        orm_mode = True


class EditAddress(BaseModel):
    longitude: Optional[confloat(gt=-180, lt=180)]
    latitude: Optional[confloat(gt=-90, lt=90)]
    complete_address: Optional[constr(min_length=5, max_length=300)]
    tag: Optional[constr(min_length=1, max_length=30)]
    floor: Optional[constr(min_length=1, max_length=50)]
    landmark: Optional[constr(min_length=1, max_length=100)]

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


class DeleteAddressResponse(BaseModel):
    message: str
