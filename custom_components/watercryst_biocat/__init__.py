"""Watercryst Biocat Integration."""
import logging
import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta

DOMAIN = "watercryst_biocat"

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Watercryst Biocat from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Lese den API-Schlüssel aus der Konfiguration
    api_key = entry.data["api_key"]

    # Erstelle einen DataUpdateCoordinator
    async def async_update_data():
        """Fetch data from the API."""
        from .sensor import fetch_data
        data = await fetch_data(api_key)
        if data is not None:
            return {"cumulativeWaterConsumption": data}
        return {}

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Watercryst Biocat",
        update_method=async_update_data,
        update_interval=timedelta(seconds=60),  # Aktualisierungsintervall auf 60 Sekunden setzen
    )

    # Erste Aktualisierung durchführen
    await coordinator.async_config_entry_first_refresh()

    # Speichere den Coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Weiterleitung an die Sensorplattform
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_forward_entry_unload(entry, "sensor"):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def fetch_data(api_key):
    """Fetch data from the Watercryst Biocat API."""
    headers = {"accept": "application/json", "x-api-key": api_key}
    url = "https://appapi.watercryst.com/v1/statistics/cumulative/daily"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                data = await response.text()  # API gibt nur einen Wert zurück, kein JSON
                _LOGGER.debug("Fetched data from API: %s", data)
                return float(data)  # Konvertiere den Wert in eine Zahl
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("Error fetching data from API: %s, status: %s, url: %s", e.message, e.status, e.request_info.url)
            return None
        except Exception as e:
            _LOGGER.error("Unexpected error: %s", e)
            return None
