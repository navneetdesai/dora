from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    TWILIO_SID: str
    TWILIO_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    EMAIL: str
    PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
