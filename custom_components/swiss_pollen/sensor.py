from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import logging
from typing import Callable

from homeassistant.components.plant import Plant
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import SwissPollenDataCoordinator
from .const import DOMAIN

from swiss_pollen import Plant

_LOGGER = logging.getLogger(__name__)


@dataclass
class SwissPollenSensorEntry:
    station: str
    plant: plant
    native_unit: str
    device_class: SensorDeviceClass
    state_class: SensorStateClass


def first_or_none(value):
    if value is None or len(value) < 1:
        return None
    return value[0]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: SwissPollenDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = []
    for station in coordinator.data.stations:
        for plant in Plant:
            sensors.append(
                SwissPollenSensorEntry(
                    station.code, plant, "No/m³", None, SensorStateClass.MEASUREMENT
                )
            )
    entities: list[SwissPollenSensorEntry] = [
        SwissPollenSensor(sensorEntry, coordinator) for sensorEntry in sensors
    ]
    async_add_entities(entities)


class SwissPollenSensor(CoordinatorEntity[SwissPollenDataCoordinator], SensorEntity):
    def __init__(
        self,
        sensor_entry: SwissPollenSensorEntry,
        coordinator: SwissPollenDataCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = SensorEntityDescription(
            key=sensor_entry.plant.name,
            name=sensor_entry.plant.description,
            native_unit_of_measurement=sensor_entry.native_unit,
            device_class=sensor_entry.device_class,
            state_class=sensor_entry.state_class,
        )
        self._sensor_entry = sensor_entry
        self._attr_name = f"{sensor_entry.plant.description} at {sensor_entry.station}"
        self._attr_unique_id = f"{sensor_entry.station}.{sensor_entry.plant.name}"
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            name=f"MeteoSwiss",
            identifiers={(DOMAIN, f"swisspollen")},
        )
        self._attr_icon = "mdi:flower-pollen"

    @property
    def native_value(self) -> StateType | Decimal:
        if self.coordinator.data is None:
            return None
        _LOGGER.info(f"%s", self.coordinator.data)
        return self.coordinator.data.measurements[
            f"{self._sensor_entry.station}-{self._sensor_entry.plant.name}"
        ].value
