import logging
import requests

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

API_URL = "https://appapi.watercryst.com/v1/measurements/direct"

def get_data(api_key):
    """Fetch data from the API."""
    try:
        response = requests.get(API_URL, headers={"x-api-key": api_key})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        _LOGGER.error("Error fetching data: %s", e)
        return {}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Watercryst Biocat sensors."""
    api_key = entry.data["api_key"]
    data = await hass.async_add_executor_job(get_data, api_key)

    sensors = []
    for key, name, unit in [
        ("waterTemp", "Public Water Temperature", "°C"),
        ("pressure", "Waterpressure to Building", "bar"),
        ("lastWaterTapVolume", "Last Water Tap Volume", "L"),
        ("lastWaterTapDuration", "Last Water Tap Duration", "s"),
    ]:
        sensors.append(WatercrystSensor(api_key, key, name, unit, data))

    async_add_entities(sensors, True)

class WatercrystSensor(SensorEntity):
    """Representation of a Watercryst sensor."""

    def __init__(self, api_key, sensor_type, name, unit, data):
        """Initialize the sensor."""
        self._api_key = api_key
        self._sensor_type = sensor_type
        self._name = name
        self._unit = unit
        self._state = data.get(sensor_type)

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
        data = get_data(self._api_key)
        self._state = data.get(self._sensor_type)
