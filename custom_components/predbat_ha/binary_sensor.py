"""Binary sensor platform for predbat_ha."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONFIG_EXPERT_MODE_SENSOR, DOMAIN
from .controller import PredbatController

# from .coordinator import PredbatDataUpdateCoordinator
from .entity import PredbatEntity

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="predbat_ha",
        name="Predbat Binary Sensor",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
    BinarySensorEntityDescription(
        key=CONFIG_EXPERT_MODE_SENSOR,
        name="Expert mode",
        # device_class=BinarySensorDeviceClass.,
    ),
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_devices):
    """Set up the binary_sensor platform."""
    # coordinator = hass.data[DOMAIN][entry.entry_id]
    controller = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        PredbatBinarySensor(
            # coordinator=coordinator,
            controller=controller,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class PredbatBinarySensor(PredbatEntity, BinarySensorEntity):
    """predbat_ha binary_sensor class."""

    def __init__(
        self,
        # coordinator: PredbatDataUpdateCoordinator,
        controller: PredbatController,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(controller = controller, entity_description = entity_description)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.controller.data.get(self.entity_description.key)
