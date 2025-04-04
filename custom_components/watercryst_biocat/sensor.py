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

SENSORS.update({
    "online": {"name": "Online-Status", "unit": None, "icon": "mdi:cloud-check"},
    "mode": {"name": "Modus", "unit": None, "icon": "mdi:water"},
    "mlState": {"name": "Mikroleckageschutz-Zustand", "unit": None, "icon": "mdi:robot"},
    "absenceModeEnabled": {"name": "Abwesenheitsmodus aktiviert", "unit": None, "icon": "mdi:shield-home"},
    "pauseLeakageProtectionUntilUTC": {"name": "Leckageschutz pausiert bis", "unit": None, "icon": "mdi:clock-outline"},
})

SENSORS.update({
    "waterTemp": {"name": "Wassertemperatur", "unit": "°C", "icon": "mdi:thermometer"},
    "pressure": {"name": "Wasserdruck", "unit": "bar", "icon": "mdi:gauge"},
    "flowRate": {"name": "Durchflussrate", "unit": "L/min", "icon": "mdi:water"},
    "lastWaterTapVolume": {"name": "Letztes Wasserzapfvolumen", "unit": "L", "icon": "mdi:cup-water"},
    "lastWaterTapDuration": {"name": "Dauer des letzten Wasserzapfens", "unit": "s", "icon": "mdi:timer"},
})

SENSORS.update({
    "dailyWaterConsumption": {"name": "Täglicher Wasserverbrauch", "unit": "L", "icon": "mdi:calendar-today"},
    "weeklyWaterConsumption": {"name": "Wöchentlicher Wasserverbrauch", "unit": "L", "icon": "mdi:calendar-week"},
    "monthlyWaterConsumption": {"name": "Monatlicher Wasserverbrauch", "unit": "L", "icon": "mdi:calendar-month"},
})

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

async def fetch_state_data(api_key):
    """Fetch state data from the Watercryst Biocat API."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    url = "https://appapi.watercryst.com/v1/state"

    async with aiohttp.ClientSession() as session:
        try:
            _LOGGER.debug("Sending request to API: %s", url)
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()  # API gibt JSON zurück
                _LOGGER.debug("Fetched state data from API: %s", data)
                return data
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error fetching state data from API: %s, status: %s, url: %s", e.message, e.status, e.request_info.url)
            return None
        except Exception as e:
            _LOGGER.error("Unexpected error: %s", e)
            return None

async def fetch_measurements_data(api_key):
    """Fetch measurement data from the Watercryst Biocat API."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    url = "https://appapi.watercryst.com/v1/measurements/direct"

    async with aiohttp.ClientSession() as session:
        try:
            _LOGGER.debug("Sending request to API: %s", url)
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()  # API gibt JSON zurück
                _LOGGER.debug("Fetched measurement data from API: %s", data)
                return data
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error fetching measurement data from API: %s, status: %s, url: %s", e.message, e.status, e.request_info.url)
            return None
        except Exception as e:
            _LOGGER.error("Unexpected error: %s", e)
            return None

async def async_update_data():
    """Fetch data from the API."""
    from .sensor import fetch_data, fetch_state_data
    _LOGGER.debug("Starting data update...")

    # Abrufen der Daten von beiden APIs
    cumulative_data = await fetch_data(api_key)
    state_data = await fetch_state_data(api_key)

    if cumulative_data is not None and state_data is not None:
        _LOGGER.debug("Data fetched successfully: cumulative=%s, state=%s", cumulative_data, state_data)
        return {
            "cumulativeWaterConsumption": cumulative_data,
            "online": state_data.get("online"),
            "mode": state_data.get("mode", {}).get("name"),
            "mlState": state_data.get("mlState"),
            "absenceModeEnabled": state_data.get("waterProtection", {}).get("absenceModeEnabled"),
            "pauseLeakageProtectionUntilUTC": state_data.get("waterProtection", {}).get("pauseLeakageProtectionUntilUTC"),
        }
    _LOGGER.warning("Failed to fetch data from one or both APIs.")
    return {}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Watercryst Biocat sensors."""
    _LOGGER.debug("Setting up sensors for Watercryst Biocat...")
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Erstelle Sensoren basierend auf den definierten SENSORS
    sensors = [
        WatercrystSensor(coordinator, sensor_type, entry.entry_id)
        for sensor_type in SENSORS
    ]
    _LOGGER.debug("Sensors created: %s", [sensor._name for sensor in sensors])
    async_add_entities(sensors)
    _LOGGER.debug("Sensors added to Home Assistant.")

class WatercrystSensor(CoordinatorEntity):
    """Representation of a Watercryst Biocat sensor."""

    def __init__(self, coordinator, sensor_type, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._name = SENSORS[sensor_type]["name"]
        self._unit = SENSORS[sensor_type]["unit"]
        self._icon = SENSORS[sensor_type]["icon"]
        self._entry_id = entry_id  # Speichere die Konfigurations-ID

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

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{self._entry_id}_{self._sensor_type}"

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        if self._sensor_type in ["cumulativeWaterConsumption", "dailyWaterConsumption", "weeklyWaterConsumption", "monthlyWaterConsumption"]:
            return "water"
        return None

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        if self._sensor_type == "cumulativeWaterConsumption":
            return "total_increasing"
        if self._sensor_type in ["dailyWaterConsumption", "weeklyWaterConsumption", "monthlyWaterConsumption"]:
            return "total"
        return None
