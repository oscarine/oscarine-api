from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from app.core import config
from app.tests.factory.cart import CartFactory
from app.tests.factory.item import ItemFactory
from app.tests.factory.owner import OwnerFactory
from app.tests.factory.shop import ShopFactory
from app.tests.factory.user import UserFactory


def test_add_item_in_cart(client: TestClient, db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop.create(db_session)
    item = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item.create(db_session)

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    post_data = {"item_id": item.id}
    headers = {'Authorization': f'Bearer {token}'}
    r = client.post(f"{config.API_V1_STR}/cart", json=post_data, headers=headers)
    response_json = r.json()
    assert r.status_code == 201
    assert response_json['item_id'] == item.id
    assert response_json['item_quantity'] == 1


def test_add_item_in_cart_when_unauthenticated(client: TestClient, db_session: Session):
    user = UserFactory()
    user.create(db_session)

    post_data = {"item_id": 1}
    r = client.post(f"{config.API_V1_STR}/cart", json=post_data)
    response_json = r.json()
    assert r.status_code == 401
    assert response_json['detail'] == 'Not authenticated'


def test_add_same_item_in_cart_error(client: TestClient, db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop.create(db_session)
    item = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item.create(db_session)

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart = CartFactory(item_id=item.id, shop_id=shop.id, user_id=user.id)
    cart.create(db_session)

    post_data = {"item_id": item.id}
    headers = {'Authorization': f'Bearer {token}'}
    r = client.post(f"{config.API_V1_STR}/cart", json=post_data, headers=headers)
    response_json = r.json()
    assert r.status_code == 400
    assert (
        response_json['detail']
        == 'CONSTRAINT_VIOLATION: Item already exist in your cart or you are trying to add item from different shops'
    )


def test_add_item_in_cart_different_shops_error(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)

    shop1 = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop1.create(db_session)
    item1 = ItemFactory(shop_id=shop1.id, owner_id=owner.id)
    item1.create(db_session)

    shop2 = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop2.create(db_session)
    item2 = ItemFactory(shop_id=shop2.id, owner_id=owner.id)
    item2.create(db_session)

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart = CartFactory(item_id=item1.id, shop_id=shop1.id, user_id=user.id)
    cart.create(db_session)

    post_data = {"item_id": item2.id}
    headers = {'Authorization': f'Bearer {token}'}
    r = client.post(f"{config.API_V1_STR}/cart", json=post_data, headers=headers)
    response_json = r.json()
    assert r.status_code == 400
    assert (
        response_json['detail']
        == 'CONSTRAINT_VIOLATION: Item already exist in your cart or you are trying to add item from different shops'
    )


def test_add_unavailable_item_in_cart_error(client: TestClient, db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop.create(db_session)
    item = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item.create(db_session)
    item.update(db_session, values={'item_available': False})

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart = CartFactory(item_id=item.id, shop_id=shop.id, user_id=user.id)
    cart.create(db_session)

    post_data = {"item_id": item.id}
    headers = {'Authorization': f'Bearer {token}'}
    r = client.post(f"{config.API_V1_STR}/cart", json=post_data, headers=headers)
    response_json = r.json()
    assert item.item_available is False
    assert r.status_code == 400
    assert (
        response_json['detail'] == 'NOT_AVAILABLE: Shop or item not available currently'
    )


def test_add_item_in_cart_from_unavailable_shop_error(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop.create(db_session)
    shop.update(db_session, values={'is_available': False})

    item = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item.create(db_session)

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart = CartFactory(item_id=item.id, shop_id=shop.id, user_id=user.id)
    cart.create(db_session)

    post_data = {"item_id": item.id}
    headers = {'Authorization': f'Bearer {token}'}
    r = client.post(f"{config.API_V1_STR}/cart", json=post_data, headers=headers)
    response_json = r.json()
    assert shop.is_available is False
    assert r.status_code == 400
    assert (
        response_json['detail'] == 'NOT_AVAILABLE: Shop or item not available currently'
    )


def test_plus_action_on_item_in_cart(client: TestClient, db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop.create(db_session)
    item = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item.create(db_session)

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart = CartFactory(item_id=item.id, shop_id=shop.id, user_id=user.id)
    cart.create(db_session)

    patch_data = {"item_id": item.id, "action": "plus"}
    headers = {'Authorization': f'Bearer {token}'}
    r = client.patch(f"{config.API_V1_STR}/cart", json=patch_data, headers=headers)
    response_json = r.json()

    db_cart_item = cart.get_by_item_id(db_session, item_id=item.id)

    assert r.status_code == 200
    assert response_json['item_id'] == item.id
    assert response_json['item_quantity'] == 2
    assert db_cart_item.item_quantity == 2


def test_minus_action_on_single_item_in_cart_error(
    client: TestClient, db_session: Session
):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop.create(db_session)
    item = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item.create(db_session)

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart = CartFactory(item_id=item.id, shop_id=shop.id, user_id=user.id)
    cart.create(db_session)

    patch_data = {"item_id": item.id, "action": "minus"}
    headers = {'Authorization': f'Bearer {token}'}
    r = client.patch(f"{config.API_V1_STR}/cart", json=patch_data, headers=headers)
    response_json = r.json()

    db_cart_item = cart.get_by_item_id(db_session, item_id=item.id)

    assert r.status_code == 400
    assert (
        response_json['detail']
        == 'INVALID_ACTION: Item quantity cannot be less than unity'
    )
    assert db_cart_item.item_quantity == 1


def test_minus_action_on_item_in_cart(client: TestClient, db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop.create(db_session)
    item = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item.create(db_session)

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart = CartFactory(item_id=item.id, shop_id=shop.id, user_id=user.id)
    cart.create(db_session)
    cart.update(db_session, values={'item_quantity': 4})

    patch_data = {"item_id": item.id, "action": "minus"}
    headers = {'Authorization': f'Bearer {token}'}
    r = client.patch(f"{config.API_V1_STR}/cart", json=patch_data, headers=headers)
    response_json = r.json()

    db_cart_item = cart.get_by_item_id(db_session, item_id=item.id)

    assert r.status_code == 200
    assert response_json['item_id'] == item.id
    assert response_json['item_quantity'] == 3
    assert db_cart_item.item_quantity == 3


def test_invalid_action_on_item_update_in_cart(client: TestClient, db_session: Session):
    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    patch_data = {"item_id": 1, "action": "invalid"}
    headers = {'Authorization': f'Bearer {token}'}
    r = client.patch(f"{config.API_V1_STR}/cart", json=patch_data, headers=headers)
    response_json = r.json()

    assert r.status_code == 422
    assert response_json['detail'][0]['loc'][0] == 'body'
    assert response_json['detail'][0]['loc'][1] == 'action'
    assert ('plus' in response_json['detail'][0]['msg']) is True
    assert ('minus' in response_json['detail'][0]['msg']) is True


def test_item_update_in_cart_when_user_unauthenticated(client: TestClient):
    patch_data = {"item_id": 1, "action": "plus"}
    r = client.patch(f"{config.API_V1_STR}/cart", json=patch_data)
    response_json = r.json()

    assert r.status_code == 401
    assert response_json['detail'] == 'Not authenticated'


def test_view_cart(client: TestClient, db_session: Session):
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

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart = CartFactory(item_id=item1.id, shop_id=shop.id, user_id=user.id)
    cart.create(db_session)
    cart.update(db_session, values={'item_quantity': 4})

    cart = CartFactory(item_id=item2.id, shop_id=shop.id, user_id=user.id)
    cart.create(db_session)
    cart.update(db_session, values={'item_quantity': 3})

    headers = {'Authorization': f'Bearer {token}'}
    r = client.get(f"{config.API_V1_STR}/cart", headers=headers)
    response_json = r.json()

    assert r.status_code == 200
    assert response_json['total_items'] == 7
    assert response_json['unique_items'] == 2
    assert response_json['total_cost'] == item1.cost * 4 + item2.cost * 3
    assert len(response_json['items']) == 2

    assert response_json['items'][0]['id'] == item1.id
    assert response_json['items'][0]['name'] == item1.name
    assert response_json['items'][0]['cost'] == item1.cost
    assert response_json['items'][0]['item_quantity'] == 4
    assert response_json['items'][0]['item_available'] is True

    assert response_json['items'][1]['id'] == item2.id
    assert response_json['items'][1]['name'] == item2.name
    assert response_json['items'][1]['cost'] == item2.cost
    assert response_json['items'][1]['item_quantity'] == 3
    assert response_json['items'][1]['item_available'] is True


def test_view_cart_when_no_items_added_error(client: TestClient, db_session: Session):
    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    headers = {'Authorization': f'Bearer {token}'}
    r = client.get(f"{config.API_V1_STR}/cart", headers=headers)
    response_json = r.json()

    assert r.status_code == 404
    assert response_json['detail'] == "EMPTY_CART"


def test_view_cart_when_user_unauthenticated_error(client: TestClient):
    r = client.get(f"{config.API_V1_STR}/cart")
    response_json = r.json()

    assert r.status_code == 401
    assert response_json['detail'] == "Not authenticated"


def test_view_cart_when_invalid_user_token_error(client: TestClient):
    headers = {'Authorization': 'Bearer invalid.auth.token'}
    r = client.get(f"{config.API_V1_STR}/cart", headers=headers)
    response_json = r.json()

    assert r.status_code == 401
    assert response_json['detail'] == "Could not validate credentials"


def test_delete_cart_item(client: TestClient, db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)
    shop = ShopFactory(
        longitude=78.0705664, latitude=27.8983082, owner_id=owner.id, radius_metres=500
    )
    shop.create(db_session)
    item = ItemFactory(shop_id=shop.id, owner_id=owner.id)
    item.create(db_session)

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart = CartFactory(item_id=item.id, shop_id=shop.id, user_id=user.id)
    cart.create(db_session)
    cart.update(db_session, values={'item_quantity': 5})

    headers = {'Authorization': f'Bearer {token}'}
    r = client.delete(f"{config.API_V1_STR}/cart/{item.id}", headers=headers)
    response_json = r.json()

    db_cart_item = cart.get_by_item_id(db_session, item_id=item.id)

    assert r.status_code == 200
    assert response_json['message'] == "DELETED"
    assert db_cart_item is None


def test_empty_current_cart(client: TestClient, db_session: Session):
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

    user = UserFactory()
    user.create(db_session)
    token = user.get_auth_token()

    cart_item1 = CartFactory(item_id=item1.id, shop_id=shop.id, user_id=user.id)
    cart_item1.create(db_session)

    cart_item2 = CartFactory(item_id=item2.id, shop_id=shop.id, user_id=user.id)
    cart_item2.create(db_session)

    headers = {'Authorization': f'Bearer {token}'}
    r = client.delete(f"{config.API_V1_STR}/cart", headers=headers)
    response_json = r.json()

    assert cart_item1.get_by_item_id(db_session, item1.id) is None
    assert cart_item2.get_by_item_id(db_session, item2.id) is None

    assert r.status_code == 200
    assert response_json["message"] == "DELETED: 2 unique items removed from cart"
