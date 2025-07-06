"""Coordinates updates for pollen data."""

import datetime
import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_PLANT_NAME, CONF_STATION_CODES, DOMAIN
from .pollen import CurrentPollen, PollenClient, Plant

DEFAULT_POLLING_INTERVAL_MINUTES = 30
MAX_POLLING_INTERVAL_MINUTES = 8 * 60

_LOGGER = logging.getLogger(__name__)


class SwissPollenDataCoordinator(DataUpdateCoordinator[CurrentPollen]):
    """Coordinates data loads for all sensors."""

    _client: PollenClient = None
    _polling_interval: int = DEFAULT_POLLING_INTERVAL_MINUTES

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        self._plant = Plant[config_entry.data.get(CONF_PLANT_NAME).upper()]
        self._station_codes = config_entry.data.get(CONF_STATION_CODES)
        self._client = PollenClient()
        update_interval = timedelta(minutes=self._polling_interval)
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
            if current_state.active is False:
                self._polling_interval = min(
                    MAX_POLLING_INTERVAL_MINUTES,
                    self._polling_interval * 2,
                )
            else:
                self._polling_interval = DEFAULT_POLLING_INTERVAL_MINUTES
            self.update_interval = timedelta(minutes=self._polling_interval)
            _LOGGER.debug(
                "Polling interval: %d min; Current state: %s",
                self._polling_interval,
                current_state,
            )
        except Exception as e:
            _LOGGER.exception(e)
            raise UpdateFailed(f"Update failed: {e}") from e

        return current_state
