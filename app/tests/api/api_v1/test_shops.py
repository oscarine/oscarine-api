from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core import config
from app.tests.factory.owner import OwnerFactory
from app.tests.factory.shop import ShopFactory


def test_get_shops_list_for_user(client: TestClient, db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=1000
    )
    shop.create(db_session)
    r = client.get(
        f"{config.API_V1_STR}/shops-list?longitude=78.06374&latitude=27.90493"
    )
    response_json = r.json()
    assert r.status_code == 200
    assert len(response_json) == 1

    response_shop = response_json[0]
    assert response_shop['id'] == shop.id
    assert response_shop['name'] == shop.name
    assert response_shop['address'] == shop.address
