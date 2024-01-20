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
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector
import homeassistant.helpers.config_validation as cv

from .const import CONFIG_INITIAL_MODE, DOMAIN, LOGGER


class PredbatConfigSchemaManager:
    """Supports the config and options flows by building schemas."""

    # TODO: COnsider using self.add_suggested_values_to_schema
    # to do the merging of existing values, as per
    # https://developers.home-assistant.io/docs/data_entry_flow_index/#defaults--suggestions
    @staticmethod
    def buildSchema(
        hass: HomeAssistant, config_entry: ConfigEntry | None = None
    ) -> vol.Schema:
        """Build config schema to be used in config and options flows."""
        schema = vol.Schema(
            {
                vol.Required(
                    "something",
                    default=None
                    if config_entry is None
                    else config_entry.data.get("something"),
                ): str,
                vol.Required(
                    CONFIG_INITIAL_MODE,
                    default="Read-only"
                    if config_entry is None
                    else config_entry.data.get(CONFIG_INITIAL_MODE),
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(
                                value="Read-only", label="Read-only"
                            ),
                            selector.SelectOptionDict(
                                value="Charge-discharge", label="Charge-discharge"
                            ),
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return schema


class PredbatConfigInputValidator:
    """Supports config and options flows by validating user input."""

    @staticmethod
    def validateInput(user_input: Dict[str, Any]):
        """Validate user input."""
        return True


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

        # TODO: Copy structure from met config flow for building
        # data structure that can be used both within config and
        # option flows.
        # TODO: Then consider how to adapt so we do the simple
        # config details first, but allow a more complex flow
        # later in the options flow

        errors = {}

        # Ensure only a single instance of Predbat is configured
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            # Do any validation in addition to what's done by
            # the schema itself
            if True:
                return self.async_create_entry(
                    # title=user_input[CONF_USERNAME],
                    title="Predbat",
                    data=user_input,
                )
            errors["somefield"] = "some_error_message"

        return self.async_show_form(
            step_id="user",
            data_schema=PredbatConfigSchemaManager.buildSchema(self.hass),
            errors=errors,
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
            # My original attempt (which works):
            # new_config_data = self.config_entry.data | user_input
            # return self.async_create_entry(
            #     title="Predbat config data",
            #     data=new_config_data,
            # )

            # This code copied from met component

            # Update config entry with data from user input
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=user_input
            )
            return self.async_create_entry(
                title=self.config_entry.title, data=user_input
            )

        # Consider using a menu like this to let the user
        # select the various parts of the system to configure
        # return self.async_show_menu(
        #     step_id="init",
        #     menu_options={
        #         "option_1": "Option 1",
        #         "option_2": "Option 2",
        #     },
        # )

        return self.async_show_form(
            step_id="init",
            data_schema=PredbatConfigSchemaManager.buildSchema(
                self.hass, self.config_entry
            ),
            errors=errors,
        )
