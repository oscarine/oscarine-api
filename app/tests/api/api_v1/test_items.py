from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core import config
from app.tests.factory.item import ItemFactory
from app.tests.factory.owner import OwnerFactory
from app.tests.factory.shop import ShopFactory


def test_get_items_for_user(client: TestClient, db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop.create(db_session)

    item1 = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item1.create(db_session)

    item2 = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item2.create(db_session)

    r = client.get(f"{config.API_V1_STR}/items-list/{shop.id}")
    response_json = r.json()

    assert r.status_code == 200
    assert len(response_json) == 2

    assert response_json[0]["id"] == item1.id
    assert response_json[0]["name"] == item1.name
    assert response_json[0]["cost"] == item1.cost
    assert response_json[0]["item_available"] is True

    assert response_json[1]["id"] == item2.id
    assert response_json[1]["name"] == item2.name
    assert response_json[1]["cost"] == item2.cost
    assert response_json[1]["item_available"] is True
