from datetime import timezone, timedelta
from typing import Any

from pydantic.env_settings import BaseSettings
from starlette.config import Config


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    WEATHER_API_KEY: str
    timezone_offset: float = +7.0  # Asia/Novosibirsk Time Zone: UTC+7
    tzinfo: timezone = timezone(timedelta(hours=timezone_offset))

    class Config:
        env_file = "src/.envs/.env"


settings: Any = Settings()
config: str = Config("src/.envs/.env")
