from pydantic.fields import Field
from typing import Any

from config.settings.base import Settings as BaseSettings


class Settings(BaseSettings):
    CORS_ALLOWED_ORIGINS: tuple[str, ...] = ()
    DEBUG = True

    PATH_TO_DATA_FILE = "test_weather.csv"
