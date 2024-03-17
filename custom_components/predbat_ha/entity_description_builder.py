"""PredbatEntityDescriptionBuilder class."""
from __future__ import annotations
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

# from homeassistant.helpers.update_coordinator import CoordinatorEntity
# from .const import DOMAIN, NAME, VERSION

# from .coordinator import PredbatDataUpdateCoordinator
# from .controller import PredbatController

from .predbat import CONFIG_ITEMS

PLATFORMS_TO_BUILD = ['switch']

class PredbatEntityDescriptionBuilder(object):
    @staticmethod
    def get_entity_descriptions_for_platform(platform: str)-> dict:
        if platform not in PLATFORMS_TO_BUILD:
            return []

        builder = PredbatEntityDescriptionBuilder()

        entity_descriptions = []
        for item in CONFIG_ITEMS:
            if item.get("type") not in platform:
                continue
            
            entity_descriptions.append(builder.get_entity_description_for_platform(item, platform))

        return entity_descriptions

    def get_entity_description_for_platform(self, item: dict[str, Any], platform: str):
        function_name_for_platform = 'get_entity_description_for_' + platform
        function_for_platform = getattr(self, function_name_for_platform)
        return function_for_platform(item)

    def get_entity_description_for_switch(self, item: dict[str, Any]):
        entity_dict = {}
        entity_dict["key"] = item.get("name")
        entity_dict["name"] = item.get("friendly_name")
        self._add_dict_item_if_key_exists("icon", item, "icon", entity_dict)

        return SwitchEntityDescription(**entity_dict)

    def _add_dict_item_if_key_exists(self, source_key: str, item: dict[str, Any], target_key: str, entity_dict: dict):
        if source_key in item:
            entity_dict[target_key] = item.get(source_key)
