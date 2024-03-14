"""PredbatEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity

# from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, NAME, VERSION

# from .coordinator import PredbatDataUpdateCoordinator
from .controller import PredbatController


# class PredbatEntity(CoordinatorEntity):
class PredbatEntity(RestoreEntity):
    """Predbat class."""

    # _attr_attribution = ATTRIBUTION

    # def __init__(self, coordinator: PredbatDataUpdateCoordinator) -> None:
    def __init__(self, controller: PredbatController) -> None:
        """Initialize."""
        # super().__init__(coordinator)
        self.controller = controller
        # self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_unique_id = controller.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
        )

    @property
    def should_poll(self):
        return False
