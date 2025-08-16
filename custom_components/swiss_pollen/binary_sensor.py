from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import SwissPollenDataCoordinator
from .const import CONF_PLANT_NAME, DOMAIN

from swiss_pollen import Plant

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: SwissPollenDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    plant: Plant = Plant[config_entry.data.get(CONF_PLANT_NAME).upper()]
    async_add_entities(
        [
            SwissPollenPlantSensor(plant, coordinator),
        ]
    )


class SwissPollenPlantSensor(
    CoordinatorEntity[SwissPollenDataCoordinator], BinarySensorEntity
):
    def __init__(
        self,
        plant: Plant,
        coordinator: SwissPollenDataCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = BinarySensorEntityDescription(
            key=f"{plant.name}-season",
            name=plant.description,
        )
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{plant.name}.season"
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            name=f"MeteoSwiss pollen for {plant.name}",
            identifiers={(DOMAIN, f"swisspollen-{plant.name}")},
        )
        self.translation_key = "season"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self.coordinator.data.is_plant_active()

    @property
    def icon(self):
        """Return the icon to use for the valve."""
        if self.is_on:
            return "mdi:tree"
        return "mdi:tree-outline"
