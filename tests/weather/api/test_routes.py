from datetime import datetime, timedelta

import pytest
import pytz
from fastapi.testclient import TestClient

from tests.helper import BaseTestClass


class TestGetForecasts(BaseTestClass):
    url = "weather/forecasts/{}/{}"

    weather_data = [
        {"event_start": "2022-01-01 01:00:40+00", "belief_horizon_in_sec": 25, "event_value": 70,  "unit": "C", "sensor": "temperature"},
        {"event_start": "2022-01-01 01:00:40+00", "belief_horizon_in_sec": 28, "event_value": 65, "unit": "W/m²", "sensor": "irradiance"},
        {"event_start": "2022-01-01 01:00:40+00", "belief_horizon_in_sec": 23, "event_value": 75, "unit": "m/s", "sensor": "wind speed"}
    ]

    @pytest.fixture
    def expected_response(self):
        return {"temperature": 70, "irradiance": 65, "wind_speed": 75}

    def test_ok(
        self,
        client: TestClient,
        expected_response,
    ):
        now = datetime(2022, 1, 1, 1, 0, 20, tzinfo=pytz.utc)
        then = now + timedelta(seconds=20)
        response = client.get(self.url.format(now.isoformat(), then.isoformat()))

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_no_forecasts_found(
        self,
        client: TestClient,
    ):
        now = datetime(2022, 1, 1, 1, 0, 20, tzinfo=pytz.utc)
        then = now + timedelta(seconds=30)
        response = client.get(self.url.format(now.isoformat(), then.isoformat()))

        assert response.status_code == 200
        assert response.json() == {"temperature": None, "irradiance": None, "wind_speed": None}


class TestGetForecastForTomorrow(BaseTestClass):
    url = "weather/forecasts/{}/"

    weather_data = [
        {"event_start": "2022-02-02 00:00:40+00", "belief_horizon_in_sec": 60, "event_value": 70,  "unit": "C", "sensor": "temperature"},
        {"event_start": "2022-02-02 00:00:40+00", "belief_horizon_in_sec": 60, "event_value": 65, "unit": "W/m²", "sensor": "irradiance"},
        {"event_start": "2022-02-02 00:00:40+00", "belief_horizon_in_sec": 60, "event_value": 75, "unit": "m/s", "sensor": "wind speed"}
    ]

    @pytest.fixture
    def expected_response(self):
        return {"sunny": False, "windy": True, "warm": True}

    def test_ok(
        self,
        client: TestClient,
        expected_response,
    ):
        now = datetime(2022, 2, 1, 23, 59, 59, tzinfo=pytz.utc)
        response = client.get(self.url.format(now.isoformat()))

        assert response.status_code == 200
        assert response.json() == expected_response
