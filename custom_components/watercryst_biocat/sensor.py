"""Sensor handling for Watercryst Biocat."""
import logging
from homeassistant.helpers.entity import Entity
import aiohttp
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)  # Logger für die Integration

API_URL = "https://appapi.watercryst.com/v1"
SENSORS = {
    "waterTemp": {"name": "Water Temperature", "unit": "°C", "icon": "mdi:thermometer"},
    "pressure": {"name": "Water Pressure", "unit": "bar", "icon": "mdi:gauge"},
    "lastWaterTapVolume": {"name": "Last Water Tap Volume", "unit": "L", "icon": "mdi:cup-water"},
    "lastWaterTapDuration": {"name": "Last Water Tap Duration", "unit": "s", "icon": "mdi:timer"},
    "totalWaterConsumptionToday": {"name": "Total Water Consumption Today", "unit": "L", "icon": "mdi:water"}
}


async def fetch_data(api_key):
    """Get data from the Watercryst Biocat API asynchronously."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}/measurements/direct", headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("API response: %s", data)  # Log the API response
                return data
        except Exception as e:
            _LOGGER.error("Error fetching data from API: %s", e)
            return {}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Watercryst Biocat sensors."""
    api_key = entry.data["api_key"]
    data = await fetch_data(api_key)

    if not data:
        _LOGGER.error("No data received from API. Sensors will not be created.")
        return

    sensors = [
        WatercrystSensor(sensor, data.get(sensor, None), api_key)
        for sensor in SENSORS
    ]
    _LOGGER.debug("Created sensors: %s", [sensor.name for sensor in sensors])
    async_add_entities(sensors)


class WatercrystSensor(Entity):
    """Representation of a Watercryst Biocat sensor."""

    def __init__(self, sensor_type, value, api_key):
        """Initialize the sensor."""
        self._sensor_type = sensor_type
        self._value = value
        self._api_key = api_key

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"sensor.{self._sensor_type}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._value

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{self._api_key}_{self._sensor_type}"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return SENSORS[self._sensor_type]["icon"]
