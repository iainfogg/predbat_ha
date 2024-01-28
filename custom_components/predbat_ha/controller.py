"""Module for controlling Predbat operations."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback

from .predbat import PredBat as OldPredbat

_LOGGER = logging.getLogger(__name__)

class PredbatController:
    """Class to control Predbat operations."""

    hass: HomeAssistant
    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialise class."""
        self.hass = hass
        self.config_entry = config_entry
        self.data = {"key": "value"}

    # @callback
    # def async_predbat_loop_service_handler(service_call):
    #     pass

    # async def async_predbat_loop(self):
    #     self.hass.async

    def load_old_predbat(self):
        old_predbat = OldPredbat(self.hass)

        # TODO: Prob need to either make initialize async, or make it sync
        # and call it as a task (or whatever the proper method is)
        old_predbat.initialize()
