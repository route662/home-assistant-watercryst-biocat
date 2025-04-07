import logging
import aiohttp
from homeassistant.components.switch import SwitchEntity
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

SWITCHES = {
    "absence_enable": {
        "name": "Enable Absence Mode",
        "url": "https://appapi.watercryst.com/v1/absence/enable",
    },
    "absence_disable": {
        "name": "Disable Absence Mode",
        "url": "https://appapi.watercryst.com/v1/absence/disable",
    },
    "leakage_pause": {
        "name": "Pause Leakage Protection",
        "url": "https://appapi.watercryst.com/v1/leakageprotection/pause",
    },
    "leakage_unpause": {
        "name": "Unpause Leakage Protection",
        "url": "https://appapi.watercryst.com/v1/leakageprotection/unpause",
    },
    "ml_measurement_start": {
        "name": "Start Micro-Leakage Measurement",
        "url": "https://appapi.watercryst.com/v1/mlmeasurement/start",
    },
    "self_test": {
        "name": "Start Self Test",
        "url": "https://appapi.watercryst.com/v1/selftest",
    },
    "water_supply_open": {
        "name": "Open Water Supply",
        "url": "https://appapi.watercryst.com/v1/watersupply/open",
    },
    "water_supply_close": {
        "name": "Close Water Supply",
        "url": "https://appapi.watercryst.com/v1/watersupply/close",
    },
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Watercryst Biocat switches."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    api_key = entry.data["api_key"]

    switches = [
        WatercrystSwitch(coordinator, api_key, switch_type, switch["name"], switch["url"], entry.entry_id)
        for switch_type, switch in SWITCHES.items()
    ]
    async_add_entities(switches)

class WatercrystSwitch(SwitchEntity):
    """Representation of a Watercryst Biocat switch."""

    def __init__(self, coordinator, api_key, switch_type, name, url, entry_id):
        """Initialize the switch."""
        self._coordinator = coordinator
        self._api_key = api_key
        self._switch_type = switch_type
        self._name = name
        self._url = url
        self._is_on = False
        self._entry_id = entry_id  # Speichere die Konfigurations-ID

    @property
    def unique_id(self):
        """Return a unique ID for the switch."""
        return f"{self._entry_id}_{self._switch_type}"

    @property
    def name(self):
        """Return the name of the switch."""
        return f"Biocat {self._name}"

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        _LOGGER.debug("Turning on %s", self._name)
        await self._send_command()
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        _LOGGER.debug("Turning off %s", self._name)
        self._is_on = False
        self.async_write_ha_state()

    async def _send_command(self):
        """Send a command to the API."""
        headers = {"accept": "application/json", "x-api-key": self._api_key}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self._url, headers=headers) as response:
                    response.raise_for_status()
                    _LOGGER.debug("Successfully sent command to %s", self._url)
            except Exception as e:
                _LOGGER.error("Failed to send command to %s: %s", self._url, e)