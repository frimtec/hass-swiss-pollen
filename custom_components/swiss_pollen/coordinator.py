"""Coordinates updates for pollen data."""

import datetime
from datetime import timedelta
import logging

from config.custom_components.swiss_pollen.const import (
    CONF_PLANT_NAME,
    CONF_STATION_CODES,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .pollen import CurrentPollen, PollenClient, Plant

_LOGGER = logging.getLogger(__name__)


class SwissPollenDataCoordinator(DataUpdateCoordinator[CurrentPollen]):
    """Coordinates data loads for all sensors."""

    _client: PollenClient = None

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        self._plant = Plant[config_entry.data.get(CONF_PLANT_NAME)]
        self._station_codes = config_entry.data.get(CONF_STATION_CODES)
        self._client = PollenClient()
        update_interval = timedelta(minutes=30)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
            always_update=False,
        )

    async def _async_update_data(self) -> CurrentPollen:
        _LOGGER.info(
            "Loading current pollen states for %s and stations %s",
            self._plant.name,
            self._station_codes,
        )
        try:
            current_state = await self.hass.async_add_executor_job(
                self._client.get_current_pollen_for_plant,
                self._plant,
                self._station_codes,
            )
            _LOGGER.debug("Current state: %s", current_state)
        except Exception as e:
            _LOGGER.exception(e)
            raise UpdateFailed(f"Update failed: {e}") from e

        return current_state
