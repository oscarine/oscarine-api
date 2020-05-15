from sqlalchemy.orm import Session

from app.models.shop import ShopRegister
from app.db_models.shop import Shop

from fastapi.encoders import jsonable_encoder


def register_new_shop(db_session: Session, *, owner_id: int,
                      data: ShopRegister) -> Shop:
    shop = Shop()
    data = jsonable_encoder(data, exclude_none=True)
    for field in data:
        if field != 'location':
            setattr(shop, field, data[field])
    shop.owner_id = owner_id
    shop.location = 'POINT({} {})'.format(data['longitude'], data['latitude'])
    db_session.add(shop)
    db_session.commit()
    db_session.refresh(shop)
    return shop
