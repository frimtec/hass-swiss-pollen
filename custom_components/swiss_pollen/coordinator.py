"""Coordinates updates for pollen data."""

import datetime
from datetime import timedelta
import logging
from random import randrange
from typing import Tuple

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .pollen import CurrentPollen, PollenClient

_LOGGER = logging.getLogger(__name__)

class SwissPollenDataCoordinator(DataUpdateCoordinator[CurrentPollen]):
    """Coordinates data loads for all sensors."""

    _client : PollenClient = None

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        self._client = PollenClient()
        update_interval = timedelta(minutes=30)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval,
                         always_update=False)

    async def _async_update_data(self) -> CurrentPollen:
        _LOGGER.info("Loading current pollen states")
        try:
            current_state = await self.hass.async_add_executor_job(
                self._client.get_current_pollen_for_all_stations)
            _LOGGER.debug("Current state: %s", current_state)
        except Exception as e:
            _LOGGER.exception(e)
            current_state = None

        return current_state