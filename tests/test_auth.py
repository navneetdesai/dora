import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_login_user(client):
    response = client.post(
        "/login",
        json={
            "username": "user1",  # pragma: allowlist secret
            "password": "password",  # pragma: allowlist secret
        },
    )
    assert response.status_code == 200
    assert response.json().get("access_token")
    assert response.json().get("token_type") == "Bearer"


@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ("firsttest55", "lasttest", 403),  # pragma: allowlist secret
        ("user2", "password", 200),  # pragma: allowlist secret
        ("firsttest55", "wrongpassword", 403),  # pragma: allowlist secret
        ("wrongusername", "lasttest", 403),  # pragma: allowlist secret
    ],
)
def test_invalid_user(client, username, password, status_code):
    response = client.post(
        "/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == status_code
