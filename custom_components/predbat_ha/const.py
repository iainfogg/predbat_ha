"""Constants for predbat_ha."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Predbat HA"
DOMAIN = "predbat_ha"
VERSION = "0.0.0"

CONFIG_INITIAL_MODE = "mode" # TODO: Delete this one
CONFIG_EXPERT_MODE_SENSOR = "switch.predbat_expert_mode" # It's actually a binary sensor in the HA integration, but the old code expects it to be a switch

CONFIG_DEPENDS_MAPPER = {
    "expert_mode": CONFIG_EXPERT_MODE_SENSOR,
    # TODO: These values must have a proper config value to go against,
    # they are all just fudged to the expert mode config for now as
    # that's all that exists
    "car_charging_manual_soc": CONFIG_EXPERT_MODE_SENSOR,
    "balance_inverters_enable": CONFIG_EXPERT_MODE_SENSOR,
    "iboost_enable": CONFIG_EXPERT_MODE_SENSOR,
}