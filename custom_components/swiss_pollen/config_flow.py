"""Config flow for Swiss Weather integration."""
from __future__ import annotations

import logging
from typing import Any

import requests
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Swiss Weather."""

    VERSION = 1

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        return self.async_create_entry(title="Swiss Pollen", data={},
                                       description=f"No")
