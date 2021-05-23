from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core import config
from app.tests.utils.shops import create_shop_with_longitude_latitude_radius


def test_get_shops_for_user_lat_long(client: TestClient, db: Session):
    longitude = 78.0705664
    latitude = 27.8983082
    radius = 1000
    shop = create_shop_with_longitude_latitude_radius(
        db=db, longitude=longitude, latitude=latitude, radius_metres=radius
    )
    r = client.get(
        f"{config.API_V1_STR}/shops-list?longitude={longitude}&latitude={latitude}"
    )
    response_json = r.json()
    assert r.status_code == 200
