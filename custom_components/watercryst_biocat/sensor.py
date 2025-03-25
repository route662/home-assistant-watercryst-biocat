"""Sensor handling for Watercryst Biocat."""
from homeassistant.helpers.entity import Entity
import requests

API_URL = "https://appapi.watercryst.com/v1"
SENSORS = {
    "waterTemp": {"name": "Water Temperature", "unit": "°C"},
    "pressure": {"name": "Water Pressure", "unit": "bar"},
    "lastWaterTapVolume": {"name": "Last Water Tap Volume", "unit": "L"},
    "lastWaterTapDuration": {"name": "Last Water Tap Duration", "unit": "s"},
    "totalWaterConsumptionToday": {"name": "Total Water Consumption Today", "unit": "L"},
}


def fetch_data(api_key):
    """Get data from the Watercryst Biocat API."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    try:
        response = requests.get(f"{API_URL}/measurements/direct", headers=headers)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()
        _LOGGER.debug("API response: %s", data)  # Log the API response
        return data
    except Exception as e:
        _LOGGER.error("Error fetching data from API: %s", e)
        return {}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Watercryst Biocat sensors."""
    api_key = entry.data["api_key"]
    data = fetch_data(api_key)

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
        self._name = SENSORS[sensor_type]["name"]
        self._unit = SENSORS[sensor_type]["unit"]
        self._api_key = api_key
        _LOGGER.debug("Initialized sensor: %s with value: %s", self._name, self._value)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Biocat {self._name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{self._api_key}_{self._sensor_type}"

    @property
    def device_info(self):
        """Return device information for the sensor."""
        return {
            "identifiers": {(DOMAIN, self._api_key)},
            "name": "Watercryst Biocat",
            "manufacturer": "Watercryst",
            "model": "Biocat",
        }
