from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core import config
from app.tests.factory.address import AddressFactory
from app.tests.factory.owner import OwnerFactory
from app.tests.factory.shop import ShopFactory
from app.tests.factory.user import UserFactory


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


def test_shop_details_for_user_longitude_latitude_param(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)
    r = client.get(
        f"{config.API_V1_STR}/shop-details?shop_id={shop.id}&longitude=78.0698410774254&latitude=27.89865957642155"
    )
    response_json = r.json()
    assert r.status_code == 200
    assert response_json["id"] == shop.id
    assert response_json["name"] == shop.name
    assert response_json["address"] == shop.address
    assert response_json["radius_metres"] == 100
    assert response_json["is_available"] is True
    assert response_json["deliverable"] is True


def test_shop_details_for_user_shop_id_capitalized(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)
    r = client.get(
        f"{config.API_V1_STR}/shop-details?shop_id={shop.id.capitalize()}&longitude=78.0698410774254&latitude=27.89865957642155"
    )
    response_json = r.json()
    assert r.status_code == 200
    assert response_json["id"] == shop.id


def test_shop_details_for_user_longitude_latitude_param_out_of_radius(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)
    r = client.get(
        f"{config.API_V1_STR}/shop-details?shop_id={shop.id}&longitude=78.06969883180747&latitude=27.89867969055395"
    )
    response_json = r.json()
    assert r.status_code == 200
    assert response_json["id"] == shop.id
    assert response_json["name"] == shop.name
    assert response_json["address"] == shop.address
    assert response_json["radius_metres"] == 100
    assert response_json["is_available"] is True
    assert response_json["deliverable"] is False


def test_shop_details_for_user_without_location_param(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)
    r = client.get(f"{config.API_V1_STR}/shop-details?shop_id={shop.id}")
    response_json = r.json()
    assert r.status_code == 200
    assert response_json["id"] == shop.id
    assert response_json["name"] == shop.name
    assert response_json["address"] == shop.address
    assert response_json["radius_metres"] == 100
    assert response_json["is_available"] is True
    assert response_json["deliverable"] is None


def test_shop_details_for_user_longitude_param_missing(client: TestClient):
    r = client.get(
        f"{config.API_V1_STR}/shop-details?shop_id=invalid-ID-slug-123456&latitude=27.89867969055395"
    )
    response_json = r.json()
    assert r.status_code == 422
    assert (
        response_json["detail"]
        == "INVALID_LOCATION: Both longitude and latitude required or neither"
    )


def test_shop_details_for_user_latitude_param_missing(client: TestClient):
    r = client.get(
        f"{config.API_V1_STR}/shop-details?shop_id=invalid-shop-id-slug-123456&longitude=78.06969883180747"
    )
    response_json = r.json()
    assert r.status_code == 422
    assert (
        response_json["detail"]
        == "INVALID_LOCATION: Both longitude and latitude required or neither"
    )


def test_shop_details_for_user_404(client: TestClient):
    r = client.get(
        f"{config.API_V1_STR}/shop-details?shop_id=invalid-shop-id-slug-123456"
    )
    response_json = r.json()
    assert r.status_code == 404
    assert response_json["detail"] == "NOT_FOUND"


def test_shop_details_for_user_address_id_param(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)

    user = UserFactory()
    user.create(db_session)

    address = AddressFactory(
        user_id=user.id, longitude=78.0698410774254, latitude=27.89865957642155
    )
    address.create(db_session)

    r = client.get(
        f"{config.API_V1_STR}/shop-details?shop_id={shop.id}&address_id={address.id}"
    )
    response_json = r.json()
    assert r.status_code == 200
    assert response_json["id"] == shop.id
    assert response_json["name"] == shop.name
    assert response_json["address"] == shop.address
    assert response_json["radius_metres"] == 100
    assert response_json["is_available"] is True
    assert response_json["deliverable"] is True


def test_shop_details_for_user_address_id_out_of_radius(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)

    user = UserFactory()
    user.create(db_session)
    address = AddressFactory(
        user_id=user.id, longitude=78.06969883180747, latitude=27.89867969055395
    )
    address.create(db_session)

    r = client.get(
        f"{config.API_V1_STR}/shop-details?shop_id={shop.id}&address_id={address.id}"
    )
    response_json = r.json()
    assert r.status_code == 200
    assert response_json["id"] == shop.id
    assert response_json["name"] == shop.name
    assert response_json["address"] == shop.address
    assert response_json["radius_metres"] == 100
    assert response_json["is_available"] is True
    assert response_json["deliverable"] is False


def test_shop_details_for_user_invalid_address_id_param(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)

    r = client.get(f"{config.API_V1_STR}/shop-details?shop_id={shop.id}&address_id=1")
    response_json = r.json()
    assert r.status_code == 422
    assert response_json["detail"] == "INVALID_LOCATION: addess_id is invalid"


def test_shop_details_for_user_shop_id_slug(client: TestClient, db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)
    r = client.get(f"{config.API_V1_STR}/shop-details?shop_id={shop.id}")
    response_json = r.json()
    assert r.status_code == 200
    assert response_json["id"] == shop.id
    assert shop.name in response_json["id"]

    random_slug_number_str: str = response_json["id"].split("-", 1)[1]
    assert len(random_slug_number_str) == 6
    assert random_slug_number_str.isdigit() is True


def test_shop_details_for_user_shop_id_slug_not_change_on_update(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)

    data = {"address": "my new shop address"}
    headers = {'Authorization': f'Bearer {owner.get_auth_token()}'}
    r = client.patch(f"{config.API_V1_STR}/shops/{shop.id}", json=data, headers=headers)
    response_json = r.json()
    after_id = response_json["id"]

    assert after_id == shop.id


def test_shop_details_for_user_shop_id_slug_change_on_name_change(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.07061944376925,
        latitude=27.89821838699808,
        owner_id=owner.id,
        radius_metres=100,
    )
    shop.create(db_session)

    data = {"name": "my new shop name"}
    headers = {'Authorization': f'Bearer {owner.get_auth_token()}'}
    r = client.patch(f"{config.API_V1_STR}/shops/{shop.id}", json=data, headers=headers)
    response_json = r.json()

    assert "my-new-shop-name-" in response_json["id"]
