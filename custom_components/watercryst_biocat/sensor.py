"""Sensor handling for Watercryst Biocat."""
import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
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

    async def async_update_data():
        """Fetch data from the API."""
        return await hass.async_add_executor_job(fetch_data, api_key)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Watercryst Biocat",
        update_method=async_update_data,
        update_interval=entry.options.get("update_interval", 60),
    )

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        _LOGGER.error("No data received from API. Sensors will not be created.")
        return

    sensors = [
        WatercrystSensor(coordinator, sensor)
        for sensor in SENSORS
    ]
    _LOGGER.debug("Created sensors: %s", [sensor.name for sensor in sensors])
    async_add_entities(sensors)


class WatercrystSensor(Entity):
    """Representation of a Watercryst Biocat sensor."""

    def __init__(self, coordinator, sensor_type):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor_type = sensor_type

    @property
    def name(self):
        """Return the name of the sensor."""
        return SENSORS[self._sensor_type]["name"]

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_type)

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{self.coordinator.api_key}_{self._sensor_type}"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return SENSORS[self._sensor_type]["icon"]

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_update(self):
        """Update the sensor."""
        await self.coordinator.async_request_refresh()
