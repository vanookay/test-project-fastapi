from typing import Any

from pydantic.env_settings import BaseSettings
from starlette.config import Config


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str
    WEATHER_API_KEY: str

    class Config:
        env_file = "src/.envs/.env"


settings: Any = Settings()
config: str = Config(".envs")
