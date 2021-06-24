from sqlalchemy.orm import Session
from sqlalchemy_utils import assert_max_length, assert_non_nullable, assert_nullable

from app.db_models.shop import Shop
from app.tests.factory.owner import OwnerFactory


def test_shop_db_model_constraints(db_session: Session):
    owner = OwnerFactory()
    owner.create(db_session)

    shop = Shop(
        name="My Shop Name",
        address="My shop address",
        owner_id=owner.id,
        location="POINT(45 32)",
        radius_metres=500,
    )
    db_session.add(shop)
    db_session.commit()

    assert_non_nullable(shop, "id")
    assert_max_length(shop, "id", 100)

    assert_non_nullable(shop, "name")
    assert_max_length(shop, "name", 50)

    assert_non_nullable(shop, "address")
    assert_max_length(shop, "address", 50)

    assert_non_nullable(shop, "owner_id")
    assert_non_nullable(shop, "location")
    assert_non_nullable(shop, "radius_metres")

    assert_nullable(shop, "phone_number")
    assert_nullable(shop, "is_available")
