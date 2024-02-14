from pydantic import BaseSettings
from pydantic.fields import Field


class Settings(BaseSettings):
    CORS_ALLOWED_ORIGINS: tuple[str, ...]
    DEBUG = False

    PATH_TO_DATA_FILE = Field("weather.csv", env=["PATH_TO_DATA_FILE"])

    TEMPERATURE_THRESHOLD: int = Field(15, env=["TEMPERATURE_THRESHOLD"])
    IRRADIANCE_THRESHOLD: int = Field(700, env=["IRRADIANCE_THRESHOLD"])
    WIND_THRESHOLD: int = Field(5, env=["WIND_THRESHOLD"])

    class Config:
        env_file = ".env"
