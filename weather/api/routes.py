from datetime import datetime

from fastapi import APIRouter

from config.settings import settings
from weather.api import schema
from weather import services

router = APIRouter()

@router.get(
    "/forecasts/{now}/{then}/",
    status_code=200,
    response_model=schema.GetForecastResponseSchema,
)
def get_forecasts_handler(
    now: datetime,
    then: datetime,
):
    """
    Given two parameters ("now" and "then", both datetimes), return the three kinds of forecasts for "then" that are the most recent, given the knowledge you can assume was available at "now".
    If any of the forecasts is not available, its value will be null.
    """

    return services.get_forecasts(now, then)


@router.get(
    "/forecasts/{now}/",
    status_code=200,
    response_model=schema.GetForecastForTomorrowResponseSchema,
)
def get_forecast_for_tomorrow(
    now: datetime,
):
    """
    Given one parameter "now", a datetime, return three booleans, telling us if the next day (the one after "now") is expected to be "warm", "sunny" and "windy". Use three internal thresholds to determine the answer and if the threshold (likely) being breached once is already enough for the boolean to be true.
    If any of the forecasts is not available, its value will be null.
    """

    return services.get_forecast_for_tomorrow(now)

__all__ = ["router"]