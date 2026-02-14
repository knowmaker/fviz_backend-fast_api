# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "FViZ"

    DATABASE_URL: AnyUrl
    SQLALCHEMY_ECHO: bool = False

    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7

    SMTP_HOST: str = "smtp.rambler.ru"
    SMTP_PORT: int = 465
    SMTP_USERNAME: str  # noreply-fviz@rambler.ru
    SMTP_PASSWORD: str  # пароль приложения/почты

    class Config:
        env_file = ".env"


settings = Settings()
