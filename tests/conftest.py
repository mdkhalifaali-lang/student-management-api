from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth_models import UserDB  # noqa: F401 - register model metadata
from database import Base, get_db
from models import StudentDB  # noqa: F401 - register model metadata


# Import the real application without running main.py's production database
# table-creation call. Each test creates tables in its own temporary database.
with patch.object(Base.metadata, "create_all"):
    from main import app


@pytest.fixture
def client(tmp_path):
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}",
        connect_args={"check_same_thread": False},
    )
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    test_engine.dispose()


@pytest.fixture
def registered_user(client):
    import uuid

    suffix = uuid.uuid4().hex
    credentials = {
        "username": f"test-user-{suffix}",
        "password": f"test-password-{suffix}",
    }
    response = client.post("/auth/register", json=credentials)
    assert response.status_code == 200
    return credentials


@pytest.fixture
def authenticated_client(client, registered_user):
    response = client.post("/auth/login", json=registered_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
