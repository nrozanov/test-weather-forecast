from typing import Optional

from pydantic import BaseModel


class GetForecastResponseSchema(BaseModel):
    temperature: Optional[int]
    irradiance: Optional[int]
    wind_speed: Optional[int]

    def __init__(self, **kwargs) -> None:
        if not kwargs.get('wind_speed') and kwargs.get('wind speed'):
            kwargs["wind_speed"] = kwargs['wind speed']

        super().__init__(**kwargs)


class GetForecastForTomorrowResponseSchema(BaseModel):
    warm: Optional[bool]
    sunny: Optional[bool]
    windy: Optional[bool]
