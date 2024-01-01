"""Module for controlling Predbat operations."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

class PredbatController:
    """Class to control Predbat operations."""

    hass: HomeAssistant
    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry
    ) -> None:
        """Initialise class."""
        self.hass = hass
        self.config_entry = config_entry
        self.data = {"key": "value"}
