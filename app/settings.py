"""
Reads environment variables from .env file and stores them in a Settings class.
"""
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Settings class that reads environment variables from .env file.
    """

    USERNAME: str
    PASSWORD: str
    HOST: str
    DATABASE: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TWILIO_SID: str
    TWILIO_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    EMAIL: str
    APP_PASSWORD: str
    SEND_EMAILS: bool = False
    SEND_TEXTS: bool = False
    PASSWORD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")

    class Config:
        env_file = ".env"


def settings() -> Settings:
    """
    Returns settings from .env file.
    :return:
    """
    return Settings()  # instantiate the Settings class
