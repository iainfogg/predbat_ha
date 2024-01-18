"""Adds config flow for Predbat."""
from __future__ import annotations

from typing import Any, Dict, Optional

import voluptuous as vol

# from homeassistant import config_entries
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    FlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import callback
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, LOGGER


class PredbatFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for Predbat."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> FlowResult:
        """Handle a flow initialized by the user.

        The config flow is a one-off process that runs on installation.
        It can't be re-run, so we should only capture things that
        will not need amending further down the line.

        Actually, that's not strictly correct. This method won't
        be able to be called again by a user without removing then
        re-adding the Predbat integration. However, this flow could
        certainly catch data using code that is then reproduced
        in the options flow, so it can be initially caught here, then
        edited later via the options flow.

        So we need to figure out what we want to catch on the initial
        adding of the integration, and what we want to save for later
        configuration.

        Maybe the initial config asks for enough to do a basic setup,
        with default values for most things, in non-expert mode.
        And other config can be modified later.
        """

        # Ensure only a single instance of Predbat is configured
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        # As we have no config to capture (as everything is in
        # the options flow), just create the config entry now.
        return self.async_create_entry(
            # title=user_input[CONF_USERNAME],
            title="Predbat",
            # data=user_input,
            data={},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return PredbatOptionsFlowHandler(config_entry)


class PredbatOptionsFlowHandler(OptionsFlow):
    """Flow handler for Predbat configuration options."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Intialise the options flow handler."""

        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """First step in the options flow."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            new_config_data = self.config_entry.data | user_input

            return self.async_create_entry(
                title="Predbat config data",
                data=new_config_data,
            )

        option_schema = vol.Schema(
            {
                vol.Required(
                    "inverter_ip_address",
                    default=self.config_entry.options.get("inverter_ip_address"),
                ): cv.string,
                vol.Optional(
                    "inverter_port",
                    default=self.config_entry.options.get("inverter_port"),
                ): cv.string,
            }
        )

        return self.async_show_form(
            step_id="init", data_schema=option_schema, errors=errors
        )
