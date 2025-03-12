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
        return response.json()
    except Exception as e:
        return {"error": str(e)}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Watercryst Biocat sensors."""
    api_key = entry.data["api_key"]
    data = fetch_data(api_key)
    sensors = [WatercrystSensor(sensor, data.get(sensor, None)) for sensor in SENSORS]
    async_add_entities(sensors)


class WatercrystSensor(Entity):
    """Representation of a Watercryst Biocat sensor."""

    def __init__(self, sensor_type, value):
        """Initialize the sensor."""
        self._sensor_type = sensor_type
        self._value = value
        self._name = SENSORS[sensor_type]["name"]
        self._unit = SENSORS[sensor_type]["unit"]

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
