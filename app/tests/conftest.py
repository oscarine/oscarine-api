from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import db_session as db_session_
from app.db.session import engine
from app.main import app


@pytest.fixture(scope='function')
def db_session() -> Generator:
    session = db_session_
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)
    engine.dispose()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
