import logging
import aiohttp
from homeassistant.components.button import ButtonEntity
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

BUTTONS = {
    "ack_event": {
        "name": "Acknowledge Event",
        "url": "https://appapi.watercryst.com/v1/ackevent",
    },
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Watercryst Biocat buttons."""
    api_key = entry.data["api_key"]

    buttons = [
        WatercrystButton(api_key, button_type, button["name"], button["url"], entry.entry_id)
        for button_type, button in BUTTONS.items()
    ]
    async_add_entities(buttons)

class WatercrystButton(ButtonEntity):
    """Representation of a Watercryst Biocat button."""

    def __init__(self, api_key, button_type, name, url, entry_id):
        """Initialize the button."""
        self._api_key = api_key
        self._button_type = button_type
        self._name = name
        self._url = url
        self._entry_id = entry_id

    @property
    def name(self):
        """Return the name of the button."""
        return f"Biocat {self._name}"

    @property
    def unique_id(self):
        """Return a unique ID for the button."""
        return f"{self._entry_id}_{self._button_type}"

    async def async_press(self):
        """Handle the button press."""
        _LOGGER.debug("Pressing button %s", self._name)
        headers = {"accept": "application/json", "x-api-key": self._api_key}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self._url, headers=headers) as response:
                    response.raise_for_status()
                    _LOGGER.debug("Successfully sent command to %s", self._url)
            except Exception as e:
                _LOGGER.error("Failed to send command to %s: %s", self._url, e)