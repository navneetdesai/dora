from pydantic import BaseSettings


class Settings(BaseSettings):
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
    send_emails: bool = False
    send_texts: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
