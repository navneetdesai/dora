from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = "localhost"
    DATABASE: str
    USERNAME: str
    PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()
