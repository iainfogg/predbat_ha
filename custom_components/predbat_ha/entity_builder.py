"""PredbatEntityDescriptionBuilder class."""
from __future__ import annotations
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

# from homeassistant.helpers.update_coordinator import CoordinatorEntity
# from .const import DOMAIN, NAME, VERSION

# from .coordinator import PredbatDataUpdateCoordinator
from .controller import PredbatController
# from .switch import PredbatSwitch

from .predbat import CONFIG_ITEMS

PLATFORMS_TO_BUILD = ['switch']

class PredbatEntityBuilder(object):
    controller: PredbatController

    def __init__(self, controller: PredbatController) -> None:
        self.controller = controller

    @staticmethod
    def get_entities_to_add_for_platform(platform: str, controller: PredbatController)-> dict:
        if platform not in PLATFORMS_TO_BUILD:
            return []

        builder = PredbatEntityBuilder(controller)

        entities_to_add = []
        for item in CONFIG_ITEMS:
            if item.get("type") not in platform:
                continue

            entities_to_add.append(builder.get_entity_to_add_for_platform(item, platform))

        return entities_to_add

    def get_entity_to_add_for_platform(self, item: dict[str, Any], platform: str):
        function_name_for_platform = 'get_entity_to_add_for_' + platform
        function_for_platform = getattr(self, function_name_for_platform)
        return function_for_platform(item)

    def get_entity_to_add_for_switch(self, item: dict[str, Any]):
        # Needed to be here instead of at the top because
        # it causes a circular import when at the top
        from .switch import PredbatSwitch

        # Build up EntityDescription
        entity_description_dict = {}
        entity_description_dict["key"] = item.get("name")
        entity_description_dict["name"] = item.get("friendly_name")
        self._add_dict_item_if_key_exists("icon", item, "icon", entity_description_dict)
        entity_description = SwitchEntityDescription(**entity_description_dict)

        # Build up Entity
        entity_dict = {}
        self._add_dict_item_if_key_exists("default", item, "initial_state", entity_dict)

        return PredbatSwitch(
            controller=self.controller,
            entity_description=entity_description,
            **entity_dict
        )

    def _add_dict_item_if_key_exists(self, source_key: str, item: dict[str, Any], target_key: str, entity_dict: dict):
        if source_key in item:
            entity_dict[target_key] = item.get(source_key)
