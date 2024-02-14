import csv
import os

import pytest

from config.settings import settings
from config.weather_data import WeatherData

class BaseTestClass():
    @pytest.fixture
    def weather_file(self):
        csv_file_path = "tests/config/test_weather_data.csv"
        with open(csv_file_path, mode='w', newline='') as file:
            fieldnames = ["event_start", "belief_horizon_in_sec", "event_value", "sensor", "unit"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(self.weather_data)

        return csv_file_path
    
    @pytest.fixture(autouse=True)
    def case_setup(self, weather_file):
        settings.PATH_TO_DATA_FILE = weather_file
        self.weather_data = WeatherData()
        yield
        os.remove(weather_file)
