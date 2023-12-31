"""Custom integration to integrate predbat_ha with Home Assistant.

For more details about this integration, please refer to
https://github.com/ludeeus/predbat_ha
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

# from homeassistant.helpers.aiohttp_client import async_get_clientsession
# from .api import PredbatApiClient
from .const import DOMAIN

# from .coordinator import PredbatDataUpdateCoordinator
from .controller import PredbatController

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = PredbatController(
        hass=hass,
        config_entry=entry,
    )

    # hass.data[DOMAIN][entry.entry_id] = coordinator = PredbatDataUpdateCoordinator(
    #     hass=hass,
    #     client=PredbatApiClient(
    #         username=entry.data[CONF_USERNAME],
    #         password=entry.data[CONF_PASSWORD],
    #         session=async_get_clientsession(hass),
    #     ),
    # )
    # # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    # await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    # An example of saving a value in an entity which is not registered
    # in the Entity Registry.
    # However, it may still persist in the UI even after being commented out
    # in code, but disappears on a force reload of the browser - this seems
    # odd behaviour.
    # hass.states.async_set("predbat_ha.mystate", "myvalue")

    # An example of removing an entity
    # hass.states.async_remove("predbat_ha.mystate")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
