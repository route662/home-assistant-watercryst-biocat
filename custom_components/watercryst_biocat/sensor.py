"""Sensor handling for Watercryst Biocat."""
import logging
from homeassistant.helpers.entity import Entity
import requests
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)  # Logger für die Integration

API_URL = "https://appapi.watercryst.com/v1"
SENSORS = {
    "waterTemp": {"name": "Wassertemperatur", "unit": "°C", "icon": "mdi:thermometer"},
    "pressure": {"name": "Wasserdruck", "unit": "bar", "icon": "mdi:gauge"},
    "lastWaterTapVolume": {"name": "Letztes Wasserzapfvolumen", "unit": "L", "icon": "mdi:cup-water"},
    "lastWaterTapDuration": {"name": "Dauer des letzten Wasserzapfens", "unit": "s", "icon": "mdi:timer"},
    "totalWaterConsumptionToday": {"name": "Gesamtwasserverbrauch heute", "unit": "L", "icon": "mdi:water"},
    "waterSupplyState": {"name": "Zustand der Wasserzufuhr", "unit": None, "icon": "mdi:water-pump"}  # Neuer Sensor
}


def fetch_data(api_key):
    """Get data from the Watercryst Biocat API."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    try:
        # Abrufen der Messdaten
        response = requests.get(f"{API_URL}/measurements/direct", headers=headers)
        response.raise_for_status()
        data = response.json()

        # Abrufen des Zustands der Wasserzufuhr
        response_state = requests.get(f"{API_URL}/state", headers=headers)
        response_state.raise_for_status()
        state_data = response_state.json()
        data["waterSupplyState"] = state_data.get("mode", {}).get("id", "unknown")

        return data
    except requests.RequestException as e:
        _LOGGER.error("Error fetching data: %s", e)
        return {}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Watercryst Biocat sensors."""
    api_key = entry.data["api_key"]
    data = await hass.async_add_executor_job(fetch_data, api_key)

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
        """Return a fixed German name for the sensor."""
        fixed_names = {
            "waterTemp": "Wassertemperatur",
            "pressure": "Wasserdruck",
            "lastWaterTapVolume": "Letztes Wasserzapfvolumen",
            "lastWaterTapDuration": "Dauer des letzten Wasserzapfens",
            "totalWaterConsumptionToday": "Gesamtwasserverbrauch heute",
            "waterSupplyState": "Zustand der Wasserzufuhr"  # Neuer Sensor
        }
        return fixed_names.get(self._sensor_type, f"Unbekannter Sensor ({self._sensor_type})")

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

    async def async_update(self):
        """Fetch new data for the sensor."""
        _LOGGER.debug("Updating sensor: %s", self._sensor_type)
        data = await hass.async_add_executor_job(fetch_data, self._api_key)
        if data:
            self._value = data.get(self._sensor_type, None)
