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
from random import uniform

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
    _attr_supported_features = WeatherEntityFeature.FORECAST_DAILY

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
    def native_temperature(self):
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

    async def async_forecast_daily(self) -> list[dict] | None:
        now = ha_now().astimezone(DEFAULT_TIME_ZONE)
        base_temp = self.native_temperature

        forecast = [
            {
                "datetime": (now + timedelta(days=0)).isoformat(),
                "condition": "sunny",
                "native_temperature": base_temp + 6,
                "native_templow": base_temp + 2,
                "precipitation_probability": 0,
                "native_precipitation": 0.0
            },
            {
                "datetime": (now + timedelta(days=1)).isoformat(),
                "condition": "partlycloudy",
                "native_temperature": base_temp,
                "native_templow": base_temp - 2,
                "precipitation_probability": 10,
                "native_precipitation": 0.1
            },
            {
                "datetime": (now + timedelta(days=2)).isoformat(),
                "condition": "cloudy",
                "native_temperature": base_temp - 3,
                "native_templow": base_temp - 5,
                "precipitation_probability": 20,
                "native_precipitation": 0.3
            },
            {
                "datetime": (now + timedelta(days=3)).isoformat(),
                "condition": "snowy" if base_temp - 6 < 0 else "rainy",
                "native_temperature": base_temp - 6,
                "native_templow": base_temp - 8,
                "precipitation_probability": 80,
                "native_precipitation": 2.5
            },
            {
                "datetime": (now + timedelta(days=4)).isoformat(),
                "condition": "partlycloudy",
                "native_temperature": base_temp - 1,
                "native_templow": base_temp - 3,
                "precipitation_probability": 30,
                "native_precipitation": 0.4
            }
        ]
        return forecast

