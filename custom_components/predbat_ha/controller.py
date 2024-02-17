"""Module for controlling Predbat operations."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .predbat import PredBat as OldPredbat
from .appdaemon_stub import AppDaemonHassStub

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

    async def load_old_predbat(self):
        old_predbat = OldPredbat(self.hass)

        # adstub = AppDaemonHassStub(self.hass)

        # result = await adstub.get_history(entity_id = 'predbat.status')
        #result = await history.get_significant_states() async_get_history('predbat.status', start_time=None, end_time=None, significant_changes_only=False, no_filter=False)
        # result = self.hass.state.data state. state.async_get_integration()
        # if result:
        #     for individual_state in result:
        #         print(f"State: {state.state}, Last changed: {state.last_changed}")

        # TODO: Prob need to either make initialize async, or make it sync
        # and call it as a task (or whatever the proper method is)
        await self.hass.async_add_executor_job(old_predbat.initialize)
