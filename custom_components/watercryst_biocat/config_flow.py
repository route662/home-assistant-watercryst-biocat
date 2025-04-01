"""Config flow for Watercryst Biocat integration."""
from homeassistant import config_entries
import voluptuous as vol
from . import DOMAIN

class WatercrystBiocatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Watercryst Biocat."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validierung des API-Schlüssels (optional)
            api_key = user_input["api_key"]
            if not api_key oder len(api_key) < 10:  # Beispielvalidierung
                errors["api_key"] = "invalid_api_key"
            else:
                # Speichere die Konfiguration
                return self.async_create_entry(
                    title="Watercryst Biocat",
                    data={
                        "api_key": user_input["api_key"],
                        "scan_interval": user_input["scan_interval"],
                    },
                )

        # Standardwerte für das Formular
        default_scan_interval = 10  # Standardintervall in Sekunden

        # Formulardefinition
        data_schema = vol.Schema(
            {
                vol.Required("api_key"): str,
                vol.Optional("scan_interval", default=default_scan_interval): vol.All(
                    vol.Coerce(int), vol.Range(min=10, max=3600)
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
