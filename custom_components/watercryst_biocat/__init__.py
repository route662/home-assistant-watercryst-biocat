"""Watercryst Biocat Integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
import requests

DOMAIN = "watercryst_biocat"
API_URL = "https://appapi.watercryst.com/v1"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Watercryst Biocat from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Register services
    async def handle_open_water_supply(call):
        api_key = call.data["api_key"]
        open_water_supply(api_key)

    async def handle_shut_off_water_supply(call):
        api_key = call.data["api_key"]
        shut_off_water_supply(api_key)

    hass.services.async_register(DOMAIN, "open_water_supply", handle_open_water_supply, schema=vol.Schema({
        vol.Required("api_key"): cv.string,
    }))

    hass.services.async_register(DOMAIN, "shut_off_water_supply", handle_shut_off_water_supply, schema=vol.Schema({
        vol.Required("api_key"): cv.string,
    }))

    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "binary_sensor"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_forward_entry_unload(entry, "sensor"):
        hass.data[DOMAIN].pop(entry.entry_id)
    if unload_ok := await hass.config_entries.async_forward_entry_unload(entry, "binary_sensor"):
        hass.data[DOMAIN].pop(entry.entry_id)

    # Unregister services
    hass.services.async_remove(DOMAIN, "open_water_supply")
    hass.services.async_remove(DOMAIN, "shut_off_water_supply")

    return unload_ok

def open_water_supply(api_key):
    """Open the water supply."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    response = requests.get(f"{API_URL}/watersupply/open", headers=headers)
    response.raise_for_status()

def shut_off_water_supply(api_key):
    """Shut off the water supply."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    response = requests.get(f"{API_URL}/watersupply/shut_off", headers=headers)
    response.raise_for_status()
