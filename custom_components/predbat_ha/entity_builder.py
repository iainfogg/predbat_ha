"""PredbatEntityDescriptionBuilder class."""
from __future__ import annotations
from typing import Any

from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.components.number import NumberEntityDescription
from homeassistant.components.number.const import NumberMode
from homeassistant.helpers import entity_registry


from .controller import PredbatController

from .const import CONFIG_DEPENDS_MAPPER, DOMAIN
from .predbat import CONFIG_ITEMS

PLATFORMS_TO_BUILD = ['switch', 'input_number']

class PredbatEntityBuilder(object):
    controller: PredbatController

    def __init__(self, controller: PredbatController) -> None:
        self.controller = controller

    @staticmethod
    async def get_entities_to_add_for_platform(platform: str, controller: PredbatController)-> dict:
        if platform not in PLATFORMS_TO_BUILD:
            return []

        builder = PredbatEntityBuilder(controller)

        entities_to_add = []
        entities_to_delete = []
        for item in CONFIG_ITEMS:
            if item.get("type") not in platform:
                continue

            # Check if this depends on another config value
            # For now, we'll not add it if it's dependent on a value
            # that's false; maybe we should create it but disable it?
            # TODO: Resolve this
            if (depends_on_predbat_entity := item.get("enable", None)):
                # Work out if the thing the item depends on is true
                if (depends_on_ha_entity := CONFIG_DEPENDS_MAPPER.get(depends_on_predbat_entity, None)):
                    # If the config value that this entity depends on is false, skip on
                    # and don't create it
                    if (builder.controller.config_entry.data.get(depends_on_ha_entity) is False):
                        # Record that this is no longer needed
                        entities_to_delete.append(item.get("name"))
                        continue
                else:
                    # Throw an error if the value in the Predbat CONFIG can't be found
                    # in our mapper that converts to HA entity names
                    raise Exception("Item {} depends on entity {} that's not found in the CONFIG_DEPENDS_MAPPER".format(item.get("name"), depends_on_predbat_entity))

            # TODO: Ensure certain items are only added when the value
            # they depend on (e.g. expert_mode) is true
            # (we are currently adding all items all the time)
            entities_to_add.append(await builder.get_entity_to_add_for_platform(item, platform))

        entity_registry_instance = entity_registry.async_get(builder.controller.hass)
        builder.controller.predbat.log("Trace: Entities being deleted as not needed {}".format(entities_to_delete))
        for entity_to_delete in entities_to_delete:
            # TODO: Not all entities are being deleted, likely due to HA naming
            # or not passing the right params into the following call
            # (failures are in log output)
            entity_entry = entity_registry_instance.async_get_entity_id(platform, DOMAIN, entity_to_delete)
            if entity_entry:
                entity_registry_instance.async_remove(entity_entry)
            else:builder.controller.predbat.log("Trace: Failed to find entity_id for {}".format(entity_to_delete))



        return entities_to_add

    async def get_entity_to_add_for_platform(self, item: dict[str, Any], platform: str):
        function_name_for_platform = 'get_entity_to_add_for_' + platform
        function_for_platform = getattr(self, function_name_for_platform)
        return await function_for_platform(item)

    async def get_entity_to_add_for_switch(self, item: dict[str, Any]):
        # Needed to be here instead of at the top because
        # it causes a circular import when at the top
        from .switch import PredbatSwitch

        # Build up EntityDescription
        entity_description_kwargs = await self._build_base_entity_description_kwargs(item)
        entity_description = SwitchEntityDescription(**entity_description_kwargs)

        # Build up Entity
        entity_dict = {}
        await self._add_dict_item_if_key_exists("default", item, "initial_state", entity_dict)

        return PredbatSwitch(
            controller=self.controller,
            entity_description=entity_description,
            **entity_dict
        )

    async def get_entity_to_add_for_input_number(self, item: dict[str, Any]):
        # Named to match predbat config, rather than actual HA platform
        # (input_number != number)
        # Needed to be here instead of at the top because
        # it causes a circular import when at the top
        from .number import PredbatNumber

        # Build up EntityDescription
        entity_description_kwargs = await self._build_base_entity_description_kwargs(item)

        await self._add_dict_item_if_key_exists("min", item, "native_min_value", entity_description_kwargs)
        await self._add_dict_item_if_key_exists("max", item, "native_max_value", entity_description_kwargs)
        await self._add_dict_item_if_key_exists("step", item, "native_step", entity_description_kwargs)
        await self._add_dict_item_if_key_exists("unit", item, "native_unit_of_measurement", entity_description_kwargs)

        if 'display_mode' in item:
            # TODO: Add display_mode values to predbat.py
            entity_description_kwargs['mode'] = NumberMode(item['display_mode'])
        else:
            # Default to input box
            entity_description_kwargs['mode'] = NumberMode('box')

        entity_description = NumberEntityDescription(**entity_description_kwargs)

        # Build up Entity
        entity_dict = {}
        await self._add_dict_item_if_key_exists("default", item, "initial_state", entity_dict)

        return PredbatNumber(
            controller=self.controller,
            entity_description=entity_description,
            **entity_dict
        )

    async def _build_base_entity_description_kwargs(self, item: dict[str, Any]):
        """Build up entity description kwargs that are common (or at least safe to use) across all entity platforms"""
        entity_description_kwargs = {}
        entity_description_kwargs["key"] = item.get("name")
        entity_description_kwargs["name"] = item.get("friendly_name")
        await self._add_dict_item_if_key_exists("icon", item, "icon", entity_description_kwargs)

        return entity_description_kwargs

    async def _add_dict_item_if_key_exists(self, source_key: str, item: dict[str, Any], target_key: str, entity_dict: dict):
        if source_key in item:
            entity_dict[target_key] = item.get(source_key)
