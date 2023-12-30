from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

class PredbatController():
    hass: HomeAssistant
    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry
    ) -> None:
        self.hass = hass
        self.config_entry = config_entry
        self.data = {"key": "value"}