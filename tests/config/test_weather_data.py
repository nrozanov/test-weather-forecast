from datetime import datetime, timedelta

import timely_beliefs as tb
from pandas import Timestamp

from config.weather_data import WeatherData
from tests.helper import BaseTestClass


class TestWeatherData(BaseTestClass):
    weather_data_dict = {
        "temperature": {"event_start": "2022-01-01 01:00:00+00", "belief_horizon_in_sec": 25, "event_value": 70,  "unit": "C"},
        "irradiance": {"event_start": "2022-01-02 01:00:00+00", "belief_horizon_in_sec": 28, "event_value": 65, "unit": "W/m²"},
        "wind speed": {"event_start": "2022-01-03 01:00:00+00", "belief_horizon_in_sec": 23, "event_value": 75, "unit": "m/s"}
    }
    weather_data = [{**data, "sensor": sensor_type} for sensor_type, data in weather_data_dict.items()]

    def test_singleton(self):
        another_weather_data = WeatherData()
        assert self.weather_data is another_weather_data, "WeatherData is a singleton"

    def test_bdf_by_sensor(self):
        bdf = self.weather_data.bdf_by_sensor

        for sensor_type, beliefs_df in bdf.items():
            assert beliefs_df.sensor.name == sensor_type, "Check sensor_type"

            assert len(beliefs_df) == 1, "Check number of rows"

            belief_row = beliefs_df.reset_index()
            event_start = datetime.strptime(
                self.weather_data_dict[sensor_type]["event_start"].replace("+00", ""), "%Y-%m-%d %H:%M:%S"
            )
            belief_horizon_in_sec = timedelta(seconds=self.weather_data_dict[sensor_type]["belief_horizon_in_sec"])
            expected_belief_time = Timestamp(event_start - belief_horizon_in_sec, tz='UTC')
            assert expected_belief_time == belief_row.loc[0, "belief_time"], "Check belief_time"
            
            