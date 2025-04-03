"""Sensor handling for Watercryst Biocat."""
import logging
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import Entity
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "waterTemp": {"name": "Wassertemperatur", "unit": "°C", "icon": "mdi:thermometer"},
    "pressure": {"name": "Wasserdruck", "unit": "bar", "icon": "mdi:gauge"},
    "flowRate": {"name": "Durchflussrate", "unit": "L/min", "icon": "mdi:water"},
    "lastWaterTapVolume": {"name": "Letztes Wasserzapfvolumen", "unit": "L", "icon": "mdi:cup-water"},
    "lastWaterTapDuration": {"name": "Dauer des letzten Wasserzapfens", "unit": "s", "icon": "mdi:timer"},
    "totalWaterConsumptionToday": {"name": "Gesamtwasserverbrauch heute", "unit": "L", "icon": "mdi:water"},
    "cumulativeWaterConsumption": {"name": "Kumulativer Wasserverbrauch", "unit": "L", "icon": "mdi:chart-bar"},
    "waterSupplyState": {"name": "Zustand der Wasserzufuhr", "unit": None, "icon": "mdi:water-pump"},
    "online": {"name": "Online-Status", "unit": None, "icon": "mdi:cloud-check"},
    "eventTitle": {"name": "Ereignistitel", "unit": None, "icon": "mdi:alert-circle"},
    "eventDescription": {"name": "Ereignisbeschreibung", "unit": None, "icon": "mdi:alert-circle-outline"},
    "absenceModeEnabled": {"name": "Abwesenheitsmodus aktiviert", "unit": None, "icon": "mdi:shield-home"},
    "pauseLeakageProtectionUntil": {"name": "Leckageschutz pausiert bis", "unit": None, "icon": "mdi:clock-outline"},
    "mlState": {"name": "Mikroleckagen-Zustand", "unit": None, "icon": "mdi:robot"},
}

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
