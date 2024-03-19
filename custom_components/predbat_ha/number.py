"""Number platform for predbat_ha."""
from __future__ import annotations

from homeassistant.components.number import NumberEntityDescription, RestoreNumber
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

# from .coordinator import PredbatDataUpdateCoordinator
from .controller import PredbatController
from .entity import PredbatEntity
from .entity_builder import PredbatEntityBuilder

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_devices):
    """Set up the number platform."""
    # coordinator = hass.data[DOMAIN][entry.entry_id]
    controller = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        PredbatEntityBuilder.get_entities_to_add_for_platform("input_number", controller)
    )

class PredbatNumber(PredbatEntity, RestoreNumber):
    """predbat_ha number class."""

    def __init__(
        self,
        controller: PredbatController,
        entity_description: NumberEntityDescription,
        initial_state = 0.0
    ) -> None:
        """Initialize the number class."""
        super().__init__(controller = controller, entity_description = entity_description)
        self.entity_description = entity_description
        self._attr_native_value = initial_state

    async def async_added_to_hass(self):
        last_state = await self.async_get_last_number_data ()
        if last_state:
            # Restore previous state
            self._attr_native_min_value = last_state.native_min_value
            self._attr_native_max_value = last_state.native_max_value
            self._attr_native_step = last_state.native_step
            self._attr_native_unit_of_measurement = last_state.native_unit_of_measurement
            self._attr_native_value = last_state.native_value

    async def async_set_native_value(self, value: float) -> None:
        """Set the number's native value."""
        self._attr_native_value = value
        await self.async_write_ha_state()

    @property
    def icon(self) -> str | None:
        """Icon of the entity"""
        self.controller.predbat.log("Trace: icon {}".format(self.entity_description.icon))
        return self.entity_description.icon
