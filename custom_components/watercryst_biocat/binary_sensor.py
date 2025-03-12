"""Binary sensor for Biocat Online & Protection modes."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from .sensor import fetch_data


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors."""
    api_key = entry.data["api_key"]
    data = fetch_data(api_key)
    async_add_entities([
        WatercrystBinarySensor("Biocat Online", data.get("online", False)),
        WatercrystBinarySensor("Microleakage Protection", data.get("waterProtection", {}).get("absenceModeEnabled", False))
    ])


class WatercrystBinarySensor(BinarySensorEntity):
    """Representation of a Watercryst Biocat binary sensor."""

    def __init__(self, name, state):
        """Initialize the binary sensor."""
        self._name = name
        self._state = state

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Biocat {self._name}"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._state

