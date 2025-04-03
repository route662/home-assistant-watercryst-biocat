"""Sensor handling for Watercryst Biocat."""
import logging
import aiohttp
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Definition der verfügbaren Sensoren
SENSORS = {
    "cumulativeWaterConsumption": {"name": "Kumulativer Wasserverbrauch", "unit": "L", "icon": "mdi:chart-bar"},
}

async def fetch_data(api_key):
    """Fetch data from the Watercryst Biocat API."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    url = "https://appapi.watercryst.com/v1/statistics/cumulative/daily"

    async with aiohttp.ClientSession() as session:
        try:
            _LOGGER.debug("Sending request to API: %s", url)
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.text()  # API gibt nur einen Wert zurück, kein JSON
                _LOGGER.debug("Fetched data from API: %s", data)
                return float(data)  # Konvertiere den Wert in eine Zahl
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error fetching data from API: %s, status: %s, url: %s", e.message, e.status, e.request_info.url)
            return None
        except Exception as e:
            _LOGGER.error("Unexpected error: %s", e)
            return None

async def async_update_data():
    """Fetch data from the API."""
    from .sensor import fetch_data
    _LOGGER.debug("Starting data update...")
    data = await fetch_data(api_key)
    if data is not None:
        _LOGGER.debug("Data fetched successfully: %s", data)
        return {"cumulativeWaterConsumption": data}
    _LOGGER.warning("No data fetched from API.")
    return {}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Watercryst Biocat sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Erstelle Sensoren basierend auf den definierten SENSORS
    sensors = [
        WatercrystSensor(coordinator, sensor_type)
        for sensor_type in SENSORS
    ]
    async_add_entities(sensors)

class WatercrystSensor(CoordinatorEntity, Entity):
    """Representation of a Watercryst Biocat sensor."""

    def __init__(self, coordinator, sensor_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._name = SENSORS[sensor_type]["name"]
        self._unit = SENSORS[sensor_type]["unit"]
        self._icon = SENSORS[sensor_type]["icon"]

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Biocat {self._name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_type)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def icon(self):
        """Return the icon for the sensor."""
        return self._icon
