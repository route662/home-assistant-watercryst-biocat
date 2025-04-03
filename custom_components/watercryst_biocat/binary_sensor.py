"""Binary sensor for Biocat Online & Protection modes."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from . import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Erstelle binäre Sensoren
    async_add_entities([
        WatercrystBinarySensor(coordinator, "online", "Biocat Online"),
        WatercrystBinarySensor(coordinator, "absenceModeEnabled", "Abwesenheitsmodus aktiviert"),
    ])

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

