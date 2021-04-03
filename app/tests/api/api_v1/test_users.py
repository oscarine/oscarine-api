from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core import config
from app.tests.utils.utils import random_email, random_lower_string


def test_register_user(client: TestClient) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(f"{config.API_V1_STR}/users", json=data)
    response_json = r.json()
    id = response_json["id"]
    assert r.status_code == 201
    assert response_json["email"] == email
    assert response_json["email_verified"] is False
    assert (isinstance(id, int) and id >= 0) is True


def test_existing_user_conflict(client: TestClient) -> None:
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password}
    r = client.post(f"{config.API_V1_STR}/users", json=data)
    assert r.status_code == 201
    r = client.post(f"{config.API_V1_STR}/users", json=data)
    response_json = r.json()
    assert r.status_code == 409
    assert response_json["detail"] == "There was a conflict with an existing user."


def test_get_user_when_not_authenticated(client: TestClient) -> None:
    r = client.get(f"{config.API_V1_STR}/users")
    response_json = r.json()
    assert r.status_code == 401
    assert response_json["detail"] == "Not authenticated"
