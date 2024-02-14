from datetime import timedelta

from config.settings import settings
from config.weather_data import WeatherData

SENSOR_TYPE_TO_FORECAST = {
    "temperature": ("warm", settings.TEMPERATURE_THRESHOLD),
    "irradiance": ("sunny", settings.IRRADIANCE_THRESHOLD),
    "wind speed": ("windy", settings.WIND_THRESHOLD)
}

def get_forecasts(now, then):
    weather_data = WeatherData()
    bdf_by_sensor = weather_data.bdf_by_sensor
    return {
        sensor_type: _get_recent_forecast_value(bdf_by_sensor[sensor_type], now, then)
            for sensor_type in weather_data.sensor_types
    }

def _get_recent_forecast_value(beliefs, now, then):
    beliefs_at_now = beliefs[beliefs.index.get_level_values('belief_time') <= now]
    try:
        recent_forecasts = beliefs_at_now.xs(then, level="event_start")
    except KeyError:
        # There are no forecasts made before now for then
        recent_forecasts = None
    
    recent_forecasts_value = None
    if recent_forecasts is not None:
        # Get forecast with the smallest belief_horizon - the most recent one
        recent_forecasts_value = recent_forecasts.sort_values(by="belief_horizon").head(1)
        recent_forecasts_value = recent_forecasts_value['event_value'].iloc[0]
    return recent_forecasts_value


def get_forecast_for_tomorrow(now):
    weather_data = WeatherData()
    bdf_by_sensor = weather_data.bdf_by_sensor
    
    return {
        key: _get_single_forecast_for_tomorrow(bdf_by_sensor[sensor_type], now, threshold)
            for sensor_type, (key, threshold) in SENSOR_TYPE_TO_FORECAST.items()
    }

def _get_single_forecast_for_tomorrow(beliefs, now, threshold):
    forecasts = beliefs[
        (beliefs.index.get_level_values('belief_time') <= now) &
        (beliefs.index.get_level_values('event_start').date == now.date() + timedelta(days=1))
    ]
    if forecasts.empty:
        return None

    if any(forecasts['event_value'] > threshold):
        return True

    return False
    
