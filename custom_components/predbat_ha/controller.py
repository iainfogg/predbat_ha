"""Module for controlling Predbat operations."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant, callback

from .predbat import PredBat as OldPredbat
from .predbat import ENVIRONMENT, ENVIRONMENT_HA_INTEGRATION

import yaml
from os import path

_LOGGER = logging.getLogger(__name__)

class PredbatController:
    """Class to control Predbat operations."""

    hass: HomeAssistant
    config_entry: ConfigEntry
    predbat: OldPredbat

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialise class."""
        self.hass = hass
        self.config_entry = config_entry
        self.data = {"key": "value"}
        self.predbat = None

    # @callback
    # def async_predbat_loop_service_handler(service_call):
    #     pass

    # async def async_predbat_loop(self):
    #     self.hass.async

    async def load_old_predbat(self):
        self.predbat = OldPredbat(self.hass)

        current_folder = path.dirname(__file__)

        file_and_folder = current_folder + '/config/apps.yaml'
        config_from_file = await self.hass.async_add_executor_job(self.config_loader, file_and_folder)

        self.predbat.args = config_from_file["pred_bat"]
        self.predbat.args[ENVIRONMENT] = ENVIRONMENT_HA_INTEGRATION

        # adstub = AppDaemonHassStub(self.hass)

        # result = await adstub.get_history(entity_id = 'predbat.status')
        #result = await history.get_significant_states() async_get_history('predbat.status', start_time=None, end_time=None, significant_changes_only=False, no_filter=False)
        # result = self.hass.state.data state. state.async_get_integration()
        # if result:
        #     for individual_state in result:
        #         print(f"State: {state.state}, Last changed: {state.last_changed}")

        # TODO: Prob need to either make initialize async, or make it sync
        # and call it as a task (or whatever the proper method is)
        async def async_run_predbat_initialize(event):
            await self.hass.async_add_executor_job(self.predbat.initialize)

        # Run the initialize once HA has started up
        # (otherwise the HA entities aren't returned, so Predbat can't find the
        # various sensors that it needs)
        self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STARTED, async_run_predbat_initialize
        )
        

    def config_loader(self, filename):
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)

        return config

