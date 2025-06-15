"""Config flow for Swiss pollen integration."""

from __future__ import annotations

import logging
from typing import Any
from swiss_pollen import Plant, Station, PollenService

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)
from homeassistant.util.location import distance
from .const import DOMAIN, CONF_PLANT_NAME, CONF_STATION_CODES

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Swiss Pollen."""

    VERSION = 3

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            try:
                stations = await self.hass.async_add_executor_job(
                    self.load_station_list
                )
                _LOGGER.debug("Stations received.", extra={"Stations": stations})
                if (
                    self.hass.config.latitude is not None
                    and self.hass.config.longitude is not None
                ):
                    stations = sorted(
                        stations, key=lambda it: self._get_distance_to_station(it)
                    )
                plant_options = [
                    SelectOptionDict(
                        value=plant.description,
                        label=self.format_plant_name_for_dropdown(plant),
                    )
                    for plant in Plant
                ]
                station_options = [
                    SelectOptionDict(
                        value=station.code,
                        label=self.format_station_name_for_dropdown(station),
                    )
                    for station in stations
                ]
                schema = vol.Schema(
                    {
                        vol.Required(CONF_PLANT_NAME): SelectSelector(
                            SelectSelectorConfig(
                                options=plant_options,
                                mode=SelectSelectorMode.DROPDOWN,
                                translation_key="plants",
                            )
                        ),
                        vol.Required(CONF_STATION_CODES): SelectSelector(
                            SelectSelectorConfig(
                                options=station_options,
                                mode=SelectSelectorMode.LIST,
                                multiple=True,
                            )
                        ),
                    }
                )
                return self.async_show_form(step_id="user", data_schema=schema)
            except Exception:
                _LOGGER.exception("Failed to retrieve station list - use all!")
                # If the API broke, we still give user the option to manually enter the
                # station code and continue.
                return self.async_show_form(
                    step_id="user", data_schema=STEP_USER_DATA_SCHEMA_BACKUP
                )

        _LOGGER.info("User chose %s", user_input)
        return self.async_create_entry(
            title="Swiss Pollen",
            data=user_input,
            description=f"{user_input[CONF_PLANT_NAME]} / {user_input[CONF_STATION_CODES]}",
        )

    def load_station_list(self) -> list[Station]:
        _LOGGER.info("Requesting stations ...")
        pollen_data = PollenService.current_values()
        return pollen_data.keys()

    def format_plant_name_for_dropdown(self, plant: Plant) -> str:
        return f"{plant.name}"

    def format_station_name_for_dropdown(self, station: Station) -> str:
        distance = self._get_distance_to_station(station)
        if distance is None:
            return f"{station.name} ({station.canton}) / alt: {station.altitude} m"
        else:
            return f"{station.name} ({station.canton}) / dist: {distance / 1000:.0f} km; alt: {station.altitude} m"

    def _get_distance_to_station(self, station: Station):
        h_lat = self.hass.config.latitude
        h_lng = self.hass.config.longitude
        if h_lat is None or h_lng is None:
            return None
        return distance(h_lat, h_lng, station.latlong[0], station.latlong[1])
