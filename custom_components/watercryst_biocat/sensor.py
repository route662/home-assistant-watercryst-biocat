"""Sensor handling for Watercryst Biocat."""
import logging
from datetime import datetime
from homeassistant.helpers.entity import Entity
import aiohttp
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)  # Logger für die Integration

API_URL = "https://appapi.watercryst.com/v1"
SENSORS = {
    "waterTemp": {"name": "Wassertemperatur", "unit": "°C", "icon": "mdi:thermometer"},
    "pressure": {"name": "Wasserdruck", "unit": "bar", "icon": "mdi:gauge"},
    "lastWaterTapVolume": {"name": "Letztes Wasserzapfvolumen", "unit": "L", "icon": "mdi:cup-water"},
    "lastWaterTapDuration": {"name": "Dauer des letzten Wasserzapfens", "unit": "s", "icon": "mdi:timer"},
    "totalWaterConsumptionToday": {"name": "Gesamtwasserverbrauch heute", "unit": "L", "icon": "mdi:water"},
    "cumulativeWaterConsumption": {"name": "Kumulativer Wasserverbrauch", "unit": "L", "icon": "mdi:chart-bar"},  # Neuer Sensor
    "waterSupplyState": {"name": "Zustand der Wasserzufuhr", "unit": None, "icon": "mdi:water-pump"},
    "online": {"name": "Online-Status", "unit": None, "icon": "mdi:cloud-check"},
    "eventTitle": {"name": "Ereignistitel", "unit": None, "icon": "mdi:alert-circle"},
    "eventDescription": {"name": "Ereignisbeschreibung", "unit": None, "icon": "mdi:alert-circle-outline"},
    "absenceModeEnabled": {"name": "Abwesenheitsmodus aktiviert", "unit": None, "icon": "mdi:shield-home"},
    "pauseLeakageProtectionUntil": {"name": "Leckageschutz pausiert bis", "unit": None, "icon": "mdi:clock-outline"},
    "mlState": {"name": "Mikroleckagen-Zustand", "unit": None, "icon": "mdi:robot"}
}


async def fetch_data(api_key):
    """Get data from the Watercryst Biocat API asynchronously."""
    _LOGGER.debug("Fetching data from API...")
    headers = {"accept": "application/json", "x-api-key": api_key}
    async with aiohttp.ClientSession() as session:
        try:
            # Abrufen der Messdaten
            async with session.get(f"{API_URL}/measurements/direct", headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("Measurements API response: %s", data)

            # Abrufen des Zustands der Wasserzufuhr
            async with session.get(f"{API_URL}/state", headers=headers) as response_state:
                response_state.raise_for_status()
                state_data = await response_state.json()
                _LOGGER.debug("State API response: %s", state_data)

                # Extrahiere zusätzliche Daten
                data["waterSupplyState"] = state_data.get("mode", {}).get("name", "Unbekannt")
                data["online"] = state_data.get("online", False)
                data["eventTitle"] = state_data.get("event", {}).get("title", "Kein Ereignis")
                data["eventDescription"] = state_data.get("event", {}).get("description", "Keine Beschreibung")
                data["absenceModeEnabled"] = state_data.get("waterProtection", {}).get("absenceModeEnabled", False)
                data["pauseLeakageProtectionUntil"] = state_data.get("waterProtection", {}).get("pauseLeakageProtectionUntilUTC", "Unbekannt")
                data["mlState"] = state_data.get("mlState", "Unbekannt")

            # Abrufen der Statistikdaten
            async with session.get(f"{API_URL}/statistics/daily/direct", headers=headers) as response_stats:
                response_stats.raise_for_status()
                stats_data = await response_stats.json()
                _LOGGER.debug("Statistics API response: %s", stats_data)

                # Berechne den heutigen Wasserverbrauch
                today = datetime.utcnow().date()
                today_consumption = next(
                    (entry["consumption"] for entry in stats_data.get("entries", []) if datetime.fromisoformat(entry["date"]).date() == today),
                    0
                )
                data["totalWaterConsumptionToday"] = today_consumption

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
        self._name = SENSORS[sensor_type]["name"]
        self._unit = SENSORS[sensor_type]["unit"]
        self._icon = SENSORS[sensor_type]["icon"]
        self._api_key = api_key
        _LOGGER.debug("Initialized sensor: %s with value: %s", self._name, self._value)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Biocat {self._name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._sensor_type == "mlState":
            # Übersetze den Wert "success" zu "Keine Leckage entdeckt"
            return "Keine Leckage entdeckt" if self._value == "success" else self._value
        return self._value

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def icon(self):
        """Return the icon for the sensor."""
        return self._icon

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
