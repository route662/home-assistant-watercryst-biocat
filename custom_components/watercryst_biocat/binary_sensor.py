"""Binary sensor for Biocat Online & Protection modes."""
from datetime import timedelta
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Watercryst Biocat from a config entry."""
    _LOGGER.debug("Setting up Watercryst Biocat integration...")
    hass.data.setdefault(DOMAIN, {})

    # Lese den API-Schlüssel aus der Konfiguration
    api_key = entry.data["api_key"]
    _LOGGER.debug("API key loaded: %s", api_key[:4] + "****")

    # Erstelle einen DataUpdateCoordinator
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

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Watercryst Biocat",
        update_method=async_update_data,
        update_interval=timedelta(seconds=60),  # Aktualisierungsintervall auf 60 Sekunden setzen
    )

    # Erste Aktualisierung durchführen
    _LOGGER.debug("Performing first data refresh...")
    await coordinator.async_config_entry_first_refresh()

    # Speichere den Coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator
    _LOGGER.debug("Coordinator stored successfully.")

    # Weiterleitung an die Sensorplattform
    _LOGGER.debug("Forwarding entry setups to sensor platform...")
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    _LOGGER.debug("Sensor platform setup complete.")
    return True

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Watercryst Biocat sensors."""
    _LOGGER.debug("Setting up sensors for Watercryst Biocat...")
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Erstelle Sensoren basierend auf den definierten SENSORS
    sensors = [
        WatercrystSensor(coordinator, sensor_type)
        for sensor_type in SENSORS
    ]
    _LOGGER.debug("Sensors created: %s", [sensor._name for sensor in sensors])
    async_add_entities(sensors)
    _LOGGER.debug("Sensors added to Home Assistant.")

class WatercrystBinarySensor(BinarySensorEntity):
    """Representation of a Watercryst Biocat binary sensor."""

    def __init__(self, coordinator, sensor_type, name):
        """Initialize the binary sensor."""
        self._coordinator = coordinator
        self._sensor_type = sensor_type
        self._name = name

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Biocat {self._name}"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._coordinator.data.get(self._sensor_type, False)

    @property
    def available(self):
        """Return if entity is available."""
        return self._coordinator.last_update_success

