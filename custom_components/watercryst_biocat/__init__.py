"""Watercryst Biocat Integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta

DOMAIN = "watercryst_biocat"

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Watercryst Biocat from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Lese den API-Schlüssel und das Abfrageintervall aus der Konfiguration
    api_key = entry.data["api_key"]
    scan_interval = entry.data.get("scan_interval", 60)  # Standard: 60 Sekunden

    # Erstelle einen DataUpdateCoordinator
    async def async_update_data():
        """Fetch data from the API."""
        from .sensor import fetch_data
        return await fetch_data(api_key)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Watercryst Biocat",
        update_method=async_update_data,
        update_interval=timedelta(seconds=scan_interval),  # Dynamisches Intervall
    )

    try:
        # Erste Aktualisierung durchführen
        await coordinator.async_config_entry_first_refresh()
    except Exception as e:
        _LOGGER.error("Failed to fetch initial data: %s", e)
        return False

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
