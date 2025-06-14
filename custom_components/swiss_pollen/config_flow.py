"""Config flow for Swiss pollen integration."""

from __future__ import annotations

import logging
from typing import Any
from swiss_pollen import Plant

import requests
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import DOMAIN, CONF_PLANT_NAME

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Swiss Pollen."""

    VERSION = 2

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            options = [
                SelectOptionDict(
                    value=plant.name, label=self.format_plant_name_for_dropdown(plant)
                )
                for plant in Plant
            ]
            schema = vol.Schema(
                {
                    vol.Required(CONF_PLANT_NAME): SelectSelector(
                        SelectSelectorConfig(
                            options=options, mode=SelectSelectorMode.DROPDOWN
                        )
                    )
                }
            )
            return self.async_show_form(step_id="user", data_schema=schema)

        _LOGGER.info("User chose %s", user_input)
        return self.async_create_entry(
            title="Swiss Pollen",
            data=user_input,
            description=f"{user_input[CONF_PLANT_NAME]}",
        )

    def format_plant_name_for_dropdown(self, plant: Plant) -> str:
        return f"{plant.name}"
