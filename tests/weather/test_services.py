from datetime import datetime, timedelta

import pytz

from tests.helper import BaseTestClass
from weather.services import get_forecasts, get_forecast_for_tomorrow

class TestGetForecasts(BaseTestClass):
    weather_data = [
        {"event_start": "2022-02-02 02:00:40+00", "belief_horizon_in_sec": 35, "event_value": 70, "sensor": "temperature", "unit": "C"},
        {"event_start": "2022-02-02 02:00:40+00", "belief_horizon_in_sec": 38, "event_value": 65, "sensor": "irradiance", "unit": "W/m²"},
        {"event_start": "2022-02-02 02:00:40+00", "belief_horizon_in_sec": 33, "event_value": 75, "sensor": "wind speed", "unit": "m/s"},
        # 
        {"event_start": "2022-02-02 02:00:40+00", "belief_horizon_in_sec": 10, "event_value": 170, "sensor": "temperature", "unit": "C"},
        {"event_start": "2022-02-02 02:00:40+00", "belief_horizon_in_sec": 10, "event_value": 165, "sensor": "irradiance", "unit": "W/m²"},
        {"event_start": "2022-01-02 02:00:40+00", "belief_horizon_in_sec": 10, "event_value": 175, "sensor": "wind speed", "unit": "m/s"},
        #
        {"event_start": "2022-02-02 02:00:39+00", "belief_horizon_in_sec": 125, "event_value": 270, "sensor": "temperature", "unit": "C"},
        {"event_start": "2022-02-02 02:00:39+00", "belief_horizon_in_sec": 128, "event_value": 265, "sensor": "irradiance", "unit": "W/m²"},
        {"event_start": "2022-01-02 02:00:39+00", "belief_horizon_in_sec": 123, "event_value": 275, "sensor": "wind speed", "unit": "m/s"}
    ]

    def test_have_all_forecasts(self):
        now = datetime(2022, 2, 2, 2, 0, 10, tzinfo=pytz.utc)
        then = now + timedelta(seconds=30)
        forecasts = get_forecasts(now, then)

        expect_forecasts = {"temperature": 70, "irradiance": 65, "wind speed": 75}
        for sensor_type, forecast in forecasts.items():
            assert forecast == expect_forecasts[sensor_type], "Check forecast value"

    def test_no_forecasts_for_then(self):
        now = datetime(2022, 2, 2, 2, 0, 10, tzinfo=pytz.utc)
        then = now + timedelta(minutes=30)
        forecasts = get_forecasts(now, then)

        for sensor_type, forecast in forecasts.items():
            assert forecast is None, "Check forecast value"

    def test_no_forecasts_for_now(self):
        now = datetime(2022, 2, 2, 1, 3, 0, tzinfo=pytz.utc)
        then = datetime(2022, 2, 2, 2, 0, 40, tzinfo=pytz.utc)
        then = now + timedelta(seconds=1)
        forecasts = get_forecasts(now, then)

        for sensor_type, forecast in forecasts.items():
            assert forecast is None, "Check forecast value"
        

class TestGetForecastForTomorrow(BaseTestClass):
    weather_data = [
        # > threshold
        {"event_start": "2022-02-02 00:00:40+00", "belief_horizon_in_sec": 60, "event_value": 65, "sensor": "irradiance", "unit": "W/m²"},
        # Makes the forecast for tomorrow sunny
        {"event_start": "2022-02-02 00:00:50+00", "belief_horizon_in_sec": 60, "event_value": 701, "sensor": "irradiance", "unit": "W/m²"},

        # Does not count as belief_time <= now
        {"event_start": "2022-02-02 00:00:40+00", "belief_horizon_in_sec": 30, "event_value": 6, "sensor": "wind speed", "unit": "m/s"},
        # < threshold
        {"event_start": "2022-02-02 00:00:40+00", "belief_horizon_in_sec": 50, "event_value": 4, "sensor": "wind speed", "unit": "m/s"},

        # Does not count as belief_time <= now
        {"event_start": "2022-02-02 00:10:00+00", "belief_horizon_in_sec": 50, "event_value": 30, "sensor": "temperature", "unit": "C"},
        # Does not count as event_start > tomorrow
        {"event_start": "2022-02-04 00:00:40+00", "belief_horizon_in_sec": 50, "event_value": 40, "sensor": "temperature", "unit": "C"},
    ]

    def test_all_cases(self):
        now = datetime(2022, 2, 1, 23, 59, 59, tzinfo=pytz.utc)
        forecasts = get_forecast_for_tomorrow(now)

        expect_forecasts = {"sunny": True, "windy": False, "warm": None}
        for sensor_type, forecast in forecasts.items():
            assert forecast == expect_forecasts[sensor_type], "Check forecast value"
            