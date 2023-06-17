import smtplib

import pytest

from app.settings import settings
from app.twilio_client import TwilioClient


@pytest.fixture
def settings_():
    return settings()


@pytest.fixture
def client():
    return TwilioClient()


def test_client(client, settings_):
    assert client.client is not None
    assert client.email == settings_.EMAIL
    assert client.password == settings_.APP_PASSWORD


def test_send_text(mocker, client):
    """
    Test send_text method
    :param mocker: Mock Twilio client
    :return: None
    """
    mock_client = mocker.patch.object(client, "client")
    mock_client.messages.create.return_value = None

    client.send_text("test", "1234567890")
    mock_client.messages.create.assert_called_once_with(
        body="test", from_=settings().TWILIO_PHONE_NUMBER, to="1234567890"
    )


def test_send_email(mocker, settings_, client):
    """
    Test send_email method
    :param mocker: Mock Twilio client
    :return: None
    """
    assert client.email == settings_.EMAIL
    assert client.password == settings_.APP_PASSWORD
    mock_client = mocker.patch.object(smtplib, "SMTP")
    mock_client.send_message.return_value = None
    client.send_email("test", "test", settings_.EMAIL)
    mock_client.assert_called_once_with("smtp.gmail.com", 587)
