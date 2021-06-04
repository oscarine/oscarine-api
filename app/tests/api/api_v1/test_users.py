from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from app.core import config
from app.core.security import verify_password
from app.tests.factory.user import UserFactory


def test_register_user(client: TestClient, db_session: Session) -> None:
    user = UserFactory()
    data = {"email": user.email, "password": user.password}
    r = client.post(f"{config.API_V1_STR}/users", json=data)
    response_json = r.json()
    id = response_json["id"]
    db_user = user.get_by_id(db_session, id)
    assert r.status_code == 201
    assert response_json["email"] == user.email
    assert response_json["email"] == db_user.email
    assert verify_password(user.password, db_user.password_hash) is True
    assert response_json["email_verified"] is False
    assert (isinstance(id, int) and id >= 0) is True


def test_existing_user_conflict(client: TestClient, db_session: Session) -> None:
    user = UserFactory()
    user.create(db_session)
    data = {"email": user.email, "password": user.password}
    r = client.post(f"{config.API_V1_STR}/users", json=data)
    response_json = r.json()
    assert r.status_code == 409
    assert response_json["detail"] == "There was a conflict with an existing user."


def test_get_user_when_not_authenticated(client: TestClient) -> None:
    r = client.get(f"{config.API_V1_STR}/users")
    response_json = r.json()
    assert r.status_code == 401
    assert response_json["detail"] == "Not authenticated"
