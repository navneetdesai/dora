import pytest
from fastapi.testclient import TestClient

from app.main import app, app_factory
from app.settings import settings

client = TestClient(app)


@pytest.fixture
def settings_():
    return settings()


def test_read_main():
    """
    Test the index route.
    :return: None
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Dora!"}


def test_app_factory():
    """
    Test the app factory function.
    :return: None
    """
    assert app_factory() is not None


def test_settings(settings_):
    """
    Test the settings
    :return:
    """
    settings_.Config.env_file = ".env"
    attributes = [
        "USERNAME",
        "PASSWORD",
        "HOST",
        "DATABASE",
        "SECRET_KEY",
        "ALGORITHM",
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "TWILIO_SID",
        "TWILIO_TOKEN",
        "TWILIO_PHONE_NUMBER",
        "EMAIL",
        "APP_PASSWORD",
        "SEND_EMAILS",
        "SEND_TEXTS",
        "PASSWORD_CONTEXT",
        "OAUTH2_SCHEME",
    ]
    for attr in attributes:
        assert hasattr(settings_, attr)
