"""Config flow for Watercryst Biocat integration."""
from homeassistant import config_entries
import voluptuous as vol

from . import DOMAIN

class WatercrystConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Watercryst Biocat."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Watercryst Biocat", data=user_input)

        return self.async_show_form(step_id="user", data_schema=vol.Schema({
            vol.Required("api_key"): str,
            vol.Required("update_interval", default=5): vol.All(vol.Coerce(int), vol.Range(min=2, max=60))
        }))

