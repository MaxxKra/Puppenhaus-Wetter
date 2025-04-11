from datetime import timedelta
from homeassistant.components.weather import WeatherEntity, WeatherEntityFeature
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfSpeed,
    UnitOfPressure,
    UnitOfLength,
    PERCENTAGE,
)
from homeassistant.util.dt import now as ha_now, DEFAULT_TIME_ZONE


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Puppenhaus Weather platform."""
    async_add_entities([PuppenhausWeather(hass)])


class PuppenhausWeather(WeatherEntity):
    _attr_name = "Puppenhaus Wetter"
    _attr_unique_id = "puppenhaus_weather"
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_humidity_unit = PERCENTAGE
    _attr_pressure_unit = UnitOfPressure.HPA
    _attr_visibility_unit = UnitOfLength.KILOMETERS
    _attr_precipitation_unit = "mm"
    _attr_supported_features = WeatherEntityFeature.FORECAST_HOURLY

    def __init__(self, hass):
        self.hass = hass

    def _get_state(self, entity_id, default=0.0):
        state = self.hass.states.get(entity_id)
        try:
            return float(state.state)
        except (ValueError, AttributeError, TypeError):
            return default

    def _get_binary(self, entity_id):
        state = self.hass.states.get(entity_id)
        return state and state.state == "on"

    def _is_day(self):
        sun = self._get_state("sensor.umwelttableau_sonnenstand")
        return sun > 0

    @property
    def temperature(self):
        return self._get_state("sensor.umwelttableau_aussentemperatur")

    @property
    def humidity(self):
        return self._get_state("sensor.umwelttableau_luftfeuchtigkeit")

    @property
    def wind_speed(self):
        return self._get_state("sensor.umwelttableau_windgeschwindigkeit")

    @property
    def wind_bearing(self):
        return 180.0  # statischer Wert oder später steuerbar

    @property
    def pressure(self):
        return 1013  # statischer Beispielwert

    @property
    def visibility(self):
        return 10  # Beispielwert in km

    @property
    def feels_like(self):
        temp = self.temperature
        humidity = self.humidity
        return round(temp - ((humidity / 100) * 2), 1)

    @property
    def condition(self):
        if self._get_binary("binary_sensor.umwelttableau_gewitter"):
            return "lightning"
        elif self._get_binary("binary_sensor.umwelttableau_regen"):
            return "rainy"
        elif self._get_binary("binary_sensor.umwelttableau_schnee"):
            return "snowy"
        else:
            wolken = self._get_state("sensor.umwelttableau_wolkendichte")
            if wolken > 70:
                return "cloudy"
            elif wolken > 30:
                return "partlycloudy"
            else:
                return "sunny" if self._is_day() else "clear-night"

    async def async_forecast_hourly(self) -> list[dict] | None:
        now = ha_now().astimezone(DEFAULT_TIME_ZONE)
        forecast = []
        for i in range(3):
            forecast.append({
                "datetime": (now + timedelta(hours=(i + 1))).isoformat(),
                "condition": "partlycloudy" if i == 0 else "rainy" if i == 1 else "cloudy",
                "native_temperature": 24 - i * 2,
                "native_apparent_temperature": 23.5 - i,
                "native_wind_speed": 10 + i * 2,
                "native_pressure": 1013,
                "humidity": 60 + i * 5,
                "cloud_coverage": 30 + i * 20,
                "precipitation_probability": 20 + i * 10,
                "native_precipitation": 0.1 * i,
                "wind_bearing": 180 + i * 10,
                "uv_index": 3.0 - i
            })
        return forecast
