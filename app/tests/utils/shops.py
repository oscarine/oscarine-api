from typing import Optional

from sqlalchemy.orm import Session

from app.crud.owner import get_by_id
from app.crud.shop import register_new_shop
from app.db_models.shop import Shop
from app.models.shop import ShopRegister
from app.tests.utils.owner import create_owner as test_create_owner
from app.tests.utils.utils import random_lower_string


def create_shop_with_longitude_latitude_radius(
    *,
    db: Session,
    owner_id: Optional[int] = None,
    longitude: float,
    latitude: float,
    radius_metres: int,
) -> Shop:
    if owner_id is None:
        owner = test_create_owner(db=db, with_verified_email=True)
    else:
        owner = get_by_id(db, owner_id=owner_id)
    new_shop_data = ShopRegister(
        name=random_lower_string(),
        longitude=longitude,
        latitude=latitude,
        address=random_lower_string(),
        radius_metres=radius_metres,
        phone_number=7675645342,
    )
    shop = register_new_shop(db, owner_id=owner.id, data=new_shop_data)
    return shop
