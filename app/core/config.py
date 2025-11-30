# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "MyProject"

    DATABASE_URL: AnyUrl
    SQLALCHEMY_ECHO: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
