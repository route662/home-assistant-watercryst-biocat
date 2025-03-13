"""Binary sensor for Biocat Online & Protection modes."""
from datetime import timedelta
import logging
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .sensor import fetch_data

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors."""
    api_key = entry.data["api_key"]
    update_interval = entry.data["update_interval"]

    async def async_update_data():
        """Fetch data from API."""
        return fetch_data(api_key)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Watercryst Biocat Binary Sensor",
        update_method=async_update_data,
        update_interval=timedelta(seconds=update_interval),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        WatercrystBinarySensor(coordinator, "Biocat Online", "online"),
        WatercrystBinarySensor(coordinator, "Microleakage Protection", "waterProtection.absenceModeEnabled")
    ])

class WatercrystBinarySensor(BinarySensorEntity):
    """Representation of a Watercryst Biocat binary sensor."""

    def __init__(self, coordinator, name, key):
        """Initialize the binary sensor."""
        self._coordinator = coordinator
        self._name = name
        self._key = key

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Biocat {self._name}"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        keys = self._key.split('.')
        value = self._coordinator.data
        for key in keys:
            value = value.get(key, {})
        return value

    @property
    def available(self):
        """Return if entity is available."""
        return self._coordinator.last_update_success

    async def async_update(self):
        """Update the entity."""
        await self._coordinator.async_request_refresh()

