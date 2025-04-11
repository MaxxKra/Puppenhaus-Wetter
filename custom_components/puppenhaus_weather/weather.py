from homeassistant.components.weather import (
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.const import TEMP_CELSIUS, SPEED_KILOMETERS_PER_HOUR, PERCENTAGE

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([PuppenhausWeather(hass)])

class PuppenhausWeather(WeatherEntity):
    _attr_name = "Puppenhaus Wetter"
    _attr_unique_id = "puppenhaus_weather"
    _attr_temperature_unit = TEMP_CELSIUS
    _attr_wind_speed_unit = SPEED_KILOMETERS_PER_HOUR
    _attr_humidity_unit = PERCENTAGE
    _attr_supported_features = WeatherEntityFeature.FORECAST

    def __init__(self, hass):
        self.hass = hass

    def _get_state(self, entity_id, default=None):
        state = self.hass.states.get(entity_id)
        return state.state if state else default

    @property
    def temperature(self):
        return float(self._get_state("sensor.umwelttableau_aussentemperatur", 0))

    @property
    def humidity(self):
        return float(self._get_state("sensor.umwelttableau_luftfeuchtigkeit", 0))

    @property
    def wind_speed(self):
        return float(self._get_state("sensor.umwelttableau_windgeschwindigkeit", 0))

    @property
    def condition(self):
        if self._get_state("binary_sensor.umwelttableau_gewitter") == "on":
            return "lightning"
        elif self._get_state("binary_sensor.umwelttableau_regen") == "on":
            return "rainy"
        elif self._get_state("binary_sensor.umwelttableau_schnee") == "on":
            return "snowy"
        else:
            wolke = float(self._get_state("sensor.umwelttableau_wolkendichte", 0))
            if wolke > 70:
                return "cloudy"
            elif wolke > 30:
                return "partlycloudy"
            else:
                return "sunny"

    @property
    def forecast(self):
        return []
