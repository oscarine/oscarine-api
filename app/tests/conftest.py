from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import scoped_session, sessionmaker

from app.db.session import engine
from app.main import app


@pytest.fixture(scope="session")
def db_engine():
    engine_ = engine

    yield engine_

    engine_.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
