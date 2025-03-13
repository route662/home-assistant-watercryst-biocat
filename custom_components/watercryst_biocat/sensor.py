"""Sensor handling for Watercryst Biocat."""
from datetime import timedelta
import logging
import requests
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

API_URL = "https://appapi.watercryst.com/v1"
SENSORS = {
    "waterTemp": {"name": "Water Temperature", "unit": "°C"},
    "pressure": {"name": "Water Pressure", "unit": "bar"},
    "lastWaterTapVolume": {"name": "Last Water Tap Volume", "unit": "L"},
    "lastWaterTapDuration": {"name": "Last Water Tap Duration", "unit": "s"},
    "totalWaterConsumptionToday": {"name": "Total Water Consumption Today", "unit": "L"},
    "waterSupplyState": {"name": "Water Supply State", "unit": None},  # Neuer Sensor
}

def fetch_data(api_key):
    """Get data from the Watercryst Biocat API."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    try:
        response = requests.get(f"{API_URL}/measurements/direct", headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Abfrage des Zustands der Wasserzufuhr
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
    update_interval = entry.data["update_interval"]

    async def async_update_data():
        """Fetch data from API."""
        return fetch_data(api_key)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Watercryst Biocat",
        update_method=async_update_data,
        update_interval=timedelta(seconds=update_interval),
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = [WatercrystSensor(coordinator, sensor) for sensor in SENSORS]
    async_add_entities(sensors)

class WatercrystSensor(Entity):
    """Representation of a Watercryst Biocat sensor."""

    def __init__(self, coordinator, sensor_type):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._sensor_type = sensor_type
        self._name = SENSORS[sensor_type]["name"]
        self._unit = SENSORS[sensor_type]["unit"]

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Biocat {self._name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._coordinator.data.get(self._sensor_type)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def available(self):
        """Return if entity is available."""
        return self._coordinator.last_update_success

    async def async_update(self):
        """Update the entity."""
        await self._coordinator.async_request_refresh()
