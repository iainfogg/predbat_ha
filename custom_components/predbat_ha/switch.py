"""Switch platform for predbat_ha."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.restore_state import RestoreEntity
from .const import DOMAIN

# from .coordinator import PredbatDataUpdateCoordinator
from .controller import PredbatController
from .entity import PredbatEntity

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="predbat_ha",
        name="Predbat Switch 1",
        icon="mdi:format-quote-close",
    ),
    SwitchEntityDescription(
        key="predbat_ha2",
        name="Predbat Switch 2",
        # icon="mdi:format-quote-close",
    ),
    # SwitchEntityDescription(
    #     key="predbat_ha",
    #     name = "expert_mode",
    #     friendly_name = "Expert Mode",
    #     type = "switch",
    #     default = False,
    # ),
    # SwitchEntityDescription(
    #     name = "active",
    #     friendly_name = "Predbat Active",
    #     type = "switch",
    #     default = False,
    # ),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_devices):
    """Set up the sensor platform."""
    # coordinator = hass.data[DOMAIN][entry.entry_id]
    controller = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        PredbatSwitch(
            controller=controller,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class PredbatSwitch(PredbatEntity, SwitchEntity):
    """predbat_ha switch class."""
    _state = False

    def __init__(
        self,
        controller: PredbatController,
        entity_description: SwitchEntityDescription,
        initial_state=False
    ) -> None:
        """Initialize the switch class."""
        super().__init__(controller)
        self.entity_description = entity_description
        # TODO this is no good here without getting the value from somewhere
        self._state = False
        self.controller.predbat.log("Trace: __init__ state {}".format(self._state))

    async def async_added_to_hass(self):
        # state = await self.async_get_last_state()
        # if state:
        # self._state = state.state == "on"
        last_state = await self.async_get_last_state()
        self.controller.predbat.log("Trace: last_state {}".format(last_state.state))
        # if last_state:
        # Restore previous state
        self._state = True if last_state.state == "on" else False
    
    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        # return self.controller.data.get("key") == "value"
        return self._state

    async def async_turn_on(self, **_: any) -> None:
        """Turn on the switch."""
        # await self.coordinator.api.async_set_title("bar")
        # await self.coordinator.async_request_refresh()
        self._state = True
        self.controller.predbat.log("Trace: Turn on _state {}".format(self._state))
        await self.async_update_ha_state()

    async def async_turn_off(self, **_: any) -> None:
        """Turn off the switch."""
        # await self.coordinator.api.async_set_title("foo")
        # await self.coordinator.async_request_refresh()
        self._state = False
        self.controller.predbat.log("Trace: Turn off _state {}".format(self._state))
        await self.async_update_ha_state()

    async def async_update_ha_state(self, *args):
        self.controller.predbat.log("Trace: args {}".format(args))
        self.async_write_ha_state()
