from typing import Dict, Optional, Tuple

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db_models.shop import Shop
from app.models.shop import ShopRegister, ShopUpdate


def register_new_shop(
    db_session: Session, *, owner_id: int, data: ShopRegister
) -> Shop:
    shop = Shop()
    data = jsonable_encoder(data, exclude_none=True)
    for field in data:
        setattr(shop, field, data[field])
    shop.owner_id = owner_id
    shop.location = 'POINT({} {})'.format(data['longitude'], data['latitude'])
    db_session.add(shop)
    db_session.commit()
    db_session.refresh(shop)
    return shop


def get_shop_by_id(db_session: Session, *, shop_id: str, owner_id: int) -> Shop:
    shop = db_session.query(Shop).filter_by(id=shop_id, owner_id=owner_id).first()
    if shop:
        return shop
    return None


def shop_details_for_user(
    db_session: Session, *, shop_id: str, location: Optional[Dict[str, float]] = None
) -> Tuple[Shop, bool]:
    shop: Shop = db_session.query(Shop).filter_by(id=shop_id).first()
    deliverable: bool = None
    if shop and location:
        longitude = location["longitude"]
        latitude = location["latitude"]
        point_ewkt = f"SRID=4326;POINT({longitude} {latitude})"
        calc_query = db_session.query(
            shop.location.ST_DWithin(
                func.ST_GeogFromText(point_ewkt), shop.radius_metres
            ).label("deliverable")
        ).one()
        deliverable = calc_query.deliverable
    return (shop, deliverable)


def shops_for_users(db_session: Session, *, longitude: float, latitude: float) -> Shop:
    point_ewkt = f'SRID=4326;POINT({longitude} {latitude})'
    shops = db_session.query(Shop).filter(
        Shop.location.ST_DWithin(func.ST_GeogFromText(point_ewkt), Shop.radius_metres)
    )
    return shops


def shop_by_id(db_session: Session, *, shop_id: str) -> Shop:
    if shop := db_session.query(Shop).filter_by(id=shop_id).first():
        return shop
    return None


def update_shop(db_session: Session, *, shop: Shop, data: ShopUpdate) -> Shop:
    data = jsonable_encoder(data, exclude_none=True)
    for field in data:
        setattr(shop, field, data[field])
    if "longitude" in data and "latitude" in data:
        shop.location = f"POINT({data['longitude']} {data['latitude']})"
    db_session.commit()
    db_session.refresh(shop)
    return shop
