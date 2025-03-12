import logging
import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import TEMP_CELSIUS, PRESSURE_BAR, VOLUME_LITERS
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_API_KEY = "api_key"
BASE_URL = "https://appapi.watercryst.com/v1/"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
})

SENSOR_TYPES = {
    "waterTemp": ["Public Water Temperature", TEMP_CELSIUS],
    "pressure": ["Waterpressure to Building", PRESSURE_BAR],
    "lastWaterTapVolume": ["Last Water Tap Volume", VOLUME_LITERS],
    "lastWaterTapDuration": ["Last Water Tap Duration", "s"],
}

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    api_key = config.get(CONF_API_KEY)
    sensors = []

    try:
        response = requests.get(BASE_URL + "measurements/direct", headers={"x-api-key": api_key})
        response.raise_for_status()
        data = response.json()

        for key, value in SENSOR_TYPES.items():
            sensors.append(WatercrystSensor(api_key, key, value[0], value[1]))

        add_entities(sensors, True)
    except Exception as e:
        _LOGGER.error("Failed to fetch data: %s", e)

class WatercrystSensor(Entity):
    """Representation of a Watercryst sensor."""

    def __init__(self, api_key, sensor_type, name, unit):
        """Initialize the sensor."""
        self._api_key = api_key
        self._sensor_type = sensor_type
        self._name = name
        self._unit = unit
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    def update(self):
        """Fetch new state data for the sensor."""
        try:
            response = requests.get(BASE_URL + "measurements/direct", headers={"x-api-key": self._api_key})
            response.raise_for_status()
            data = response.json()
            self._state = data.get(self._sensor_type)
        except Exception as e:
            _LOGGER.error("Error updating sensor: %s", e)

