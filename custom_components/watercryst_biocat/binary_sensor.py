"""Binary sensor for Biocat Online & Protection modes."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from . import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        WatercrystBinarySensor(coordinator, "Biocat Online", "online"),
        WatercrystBinarySensor(coordinator, "Microleakage Protection", "absenceModeEnabled")
    ])

class WatercrystBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Watercryst Biocat binary sensor."""

    def __init__(self, coordinator, name, sensor_type):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._name = name
        self._sensor_type = sensor_type

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Biocat {self._name}"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self.coordinator.data.get(self._sensor_type)
