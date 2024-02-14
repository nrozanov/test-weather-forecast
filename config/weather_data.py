import pandas as pd
import timely_beliefs as tb

from config.settings import settings

class WeatherData:
    """
    Singleton class to load the weather data from the CSV file, create a BeliefsDataFrame and store it
    """
    _instance = None
    
    sensor_types = ("irradiance", "temperature", "wind speed")

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def bdf_by_sensor(self):
        return self._bdf_by_sensor

    def __init__(self):
        df = self._build_data_frame()
        self._bdf_by_sensor = self._build_timely_believes(df)

    def _build_data_frame(self):
        df = pd.read_csv(settings.PATH_TO_DATA_FILE)
        
        df['event_start'] = pd.to_datetime(df['event_start'])
        df['belief_horizon'] = pd.to_timedelta(df['belief_horizon_in_sec'], unit='s')
        df['belief_time'] = df['event_start'] - df['belief_horizon']
        return df.drop(columns=['belief_horizon_in_sec'])
    
    def _build_timely_believes(self, df):
        return {
            sensor_type: self._create_timely_belief(df, sensor_type)
                for sensor_type in self.sensor_types
        }

    def _create_timely_belief(self, df, sensor_type: str):
        df_filtered = df[df['sensor'] == sensor_type]
        bdf = tb.BeliefsDataFrame(
            df_filtered, sensor=tb.Sensor(sensor_type), source=tb.BeliefSource(f"Source {sensor_type}")
        )
        return bdf
        
