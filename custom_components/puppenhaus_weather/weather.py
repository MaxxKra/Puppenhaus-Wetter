from datetime import timedelta
from homeassistant.components.weather import WeatherEntity
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfSpeed,
    UnitOfPressure,
    UnitOfLength,
    PERCENTAGE,
)
from homeassistant.util.dt import now as ha_now


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
    _attr_precipitation_unit = "mm"  # Als Text, da kein Enum

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
        return 180.0  # Optional: z. B. aus Drehregler

    @property
    def pressure(self):
        return 1013  # Optional statisch

    @property
    def visibility(self):
        return 10  # Sichtweite in km

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

    @property
    def forecast(self):
        now = ha_now()
        return [
            {
                "datetime": (now + timedelta(hours=3)).isoformat(),
                "temperature": 24,
                "condition": "partlycloudy",
                "precipitation": 0.0,
                "wind_speed": 10.0,
                "wind_bearing": 180
            },
            {
                "datetime": (now + timedelta(hours=6)).isoformat(),
                "temperature": 20,
                "condition": "rainy",
                "precipitation": 1.2,
                "wind_speed": 12.0,
                "wind_bearing": 190
            },
            {
                "datetime": (now + timedelta(hours=9)).isoformat(),
                "temperature": 17,
                "condition": "cloudy",
                "precipitation": 0.3,
                "wind_speed": 8.0,
                "wind_bearing": 200
            },
        ]
