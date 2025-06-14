from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import logging
from typing import Callable

from config.custom_components.swiss_pollen.const import CONF_PLANT_NAME
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

from swiss_pollen import Plant, Level, Station

_LOGGER = logging.getLogger(__name__)


@dataclass
class SwissPollenSensorEntry:
    station: Station
    plant: Plant
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
    plant: Plant = Plant[config_entry.data.get(CONF_PLANT_NAME)]

    numeric_sensors = []
    for station in coordinator.data.stations:
        numeric_sensors.append(
            SwissPollenSensorEntry(
                station, plant, "No/m³", None, SensorStateClass.MEASUREMENT
            )
        )

    level_sensors = []
    for station in coordinator.data.stations:
        level_sensors.append(
            SwissPollenSensorEntry(station, plant, None, SensorDeviceClass.ENUM, None)
        )

    numeric_entities: list[SwissPollenSensorEntry] = [
        SwissPollenNumericSensor(plant, sensorEntry, coordinator)
        for sensorEntry in numeric_sensors
    ]
    level_entities: list[SwissPollenSensorEntry] = [
        SwissPollenLevelSensor(plant, sensorEntry, coordinator)
        for sensorEntry in level_sensors
    ]
    async_add_entities(numeric_entities + level_entities)


class SwissPollenNumericSensor(
    CoordinatorEntity[SwissPollenDataCoordinator], SensorEntity
):
    def __init__(
        self,
        plant: Plant,
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
        self._attr_name = (
            f"{sensor_entry.plant.description} @ {sensor_entry.station.name}"
        )
        self._attr_unique_id = f"{sensor_entry.station.code}.{sensor_entry.plant.name}"
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            name=f"MeteoSwiss pollen for {plant.name}",
            identifiers={(DOMAIN, f"swisspollen-{plant.name}")},
        )
        self._attr_icon = "mdi:flower-pollen"

    @property
    def native_value(self) -> StateType | Decimal:
        if self.coordinator.data is None:
            return None
        measurement = self.coordinator.data.measurements.get(
            f"{self._sensor_entry.station.code}-{self._sensor_entry.plant.name}", None
        )
        return measurement.value if measurement is not None else None


class SwissPollenLevelSensor(
    CoordinatorEntity[SwissPollenDataCoordinator], SensorEntity
):
    def __init__(
        self,
        plant: Plant,
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
        self._attr_name = (
            f"{sensor_entry.plant.description} @ {sensor_entry.station.name} (Level)"
        )
        self._attr_unique_id = (
            f"{sensor_entry.station.code}.{sensor_entry.plant.name}.level"
        )
        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            name=f"MeteoSwiss pollen for {plant.name}",
            identifiers={(DOMAIN, f"swisspollen-{plant.name}")},
        )
        self._attr_options = [
            "none",
            "low",
            "medium",
            "strong",
            "very_strong",
        ]
        self._attr_translation_key = "level"
        self._attr_icon = "mdi:flag"

    @property
    def native_value(self) -> StateType | str:
        if self.coordinator.data is None:
            return None
        measurement = self.coordinator.data.measurements.get(
            f"{self._sensor_entry.station.code}-{self._sensor_entry.plant.name}", None
        )
        return (
            Level.level(measurement.value).description
            if measurement is not None
            else None
        )
