"""Switch platform for predbat_ha."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

# from .coordinator import PredbatDataUpdateCoordinator
from .controller import PredbatController
from .entity import PredbatEntity
from .entity_builder import PredbatEntityBuilder

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="switch.predbat_switch_no_1",
        name="pb_sw_1",
        icon="mdi:format-quote-close",
    ),
    SwitchEntityDescription(
        key="switch.predbat_switch_no_2",
        name="pb_sw_2",
        icon="mdi:format-quote-close",
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
        PredbatEntityBuilder.get_entities_to_add_for_platform("switch", controller)
    )


class PredbatSwitch(PredbatEntity, SwitchEntity, RestoreEntity):
    """predbat_ha switch class."""

    def __init__(
        self,
        controller: PredbatController,
        entity_description: SwitchEntityDescription,
        initial_state=False
    ) -> None:
        """Initialize the switch class."""
        super().__init__(controller = controller, entity_description = entity_description)
        self.entity_description = entity_description
        # TODO this is no good here without getting the value from somewhere
        self._attr_is_on = initial_state

    async def async_added_to_hass(self):
        last_state = await self.async_get_last_state()
        if last_state:
            # Restore previous state
            self._attr_is_on = True if last_state.state == "on" else False

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        # return self.controller.data.get("key") == "value"
        return self._attr_is_on

    async def async_turn_on(self, **_: any) -> None:
        """Turn on the switch."""
        self._attr_is_on = True
        await self.async_update_ha_state()

    async def async_turn_off(self, **_: any) -> None:
        """Turn off the switch."""
        self._attr_is_on = False
        await self.async_update_ha_state()

    # TODO Rename this to avoid clash with HA name (for readability if nothing else)
    async def async_update_ha_state(self, *args):
        self.async_write_ha_state()

    @property
    def icon(self) -> str | None:
        """Icon of the entity"""
        return self.entity_description.icon
