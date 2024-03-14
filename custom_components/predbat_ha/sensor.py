"""Sensor platform for predbat_ha."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant

from .const import DOMAIN

# from .coordinator import PredbatDataUpdateCoordinator
from .controller import PredbatController
from .entity import PredbatEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="predbat_ha",
        name="Predbat Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_devices):
    """Set up the sensor platform."""
    # coordinator = hass.data[DOMAIN][entry.entry_id]
    controller = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        PredbatSensor(
            # coordinator=coordinator,
            controller=controller,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class PredbatSensor(PredbatEntity, SensorEntity):
    """predbat_ha Sensor class."""

    def __init__(
        self,
        # coordinator: PredbatDataUpdateCoordinator,
        controller: PredbatController,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(controller = controller, entity_description = entity_description)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self.controller.data.get("key")
