from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import EntityCategory

from . import SwissPollenDataCoordinator
from .const import CONF_PLANT_NAME, CONF_STATION_CODES, DOMAIN

from swiss_pollen import Plant, Level, Station, StationState

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
    plant: Plant = Plant[config_entry.data.get(CONF_PLANT_NAME).upper()]
    station_codes: Plant = config_entry.data.get(CONF_STATION_CODES)

    numeric_sensors = []
    level_sensors = []
    station_state_sensors = []
    for station_code in station_codes:
        if station_code in station_codes:
            station = coordinator.data.station_by_code(station_code)
            numeric_sensors.append(
                SwissPollenSensorEntry(
                    station, plant, "No/m³", None, SensorStateClass.MEASUREMENT
                )
            )
            level_sensors.append(
                SwissPollenSensorEntry(
                    station, plant, None, SensorDeviceClass.ENUM, None
                )
            )
            station_state_sensors.append(
                SwissPollenSensorEntry(
                    station, plant, None, SensorDeviceClass.ENUM, None
                )
            )

    numeric_entities: list[SwissPollenSensorEntry] = [
        SwissPollenNumericSensor(plant, sensorEntry, coordinator)
        for sensorEntry in numeric_sensors
    ]
    level_entities: list[SwissPollenSensorEntry] = [
        SwissPollenLevelSensor(plant, sensorEntry, coordinator)
        for sensorEntry in level_sensors
    ]
    station_states_entities: list[SwissPollenSensorEntry] = [
        SwissPollenStationStateSensor(plant, sensorEntry, coordinator)
        for sensorEntry in station_state_sensors
    ]
    async_add_entities(
        numeric_entities
        + level_entities
        + station_states_entities
        + [SwissPollenVersionSensor(plant, coordinator)]
    )


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
        self._attr_has_entity_name = True
        self.translation_key = f"{sensor_entry.station.code.lower()}_numeric"
        self._attr_unique_id = f"{sensor_entry.station.code}.{sensor_entry.plant.name}"
        self._attr_device_info = SwissPollenDataCoordinator.device_info(plant)
        self._attr_icon = "mdi:flower-pollen"

    @property
    def native_value(self) -> StateType | Decimal:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.value_by_station(self._sensor_entry.station)


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
        self._attr_has_entity_name = True
        self.translation_key = f"{sensor_entry.station.code.lower()}_level"
        self._attr_unique_id = (
            f"{sensor_entry.station.code}.{sensor_entry.plant.name}.level"
        )
        self._attr_device_info = SwissPollenDataCoordinator.device_info(plant)
        self._attr_options = [
            "none",
            "low",
            "medium",
            "strong",
            "very_strong",
        ]
        self._attr_icon = "mdi:flag"

    @property
    def native_value(self) -> StateType | str:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.level_by_station(self._sensor_entry.station)


class SwissPollenStationStateSensor(
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
            entity_category=EntityCategory.DIAGNOSTIC,
        )
        self._sensor_entry = sensor_entry
        self._attr_has_entity_name = True
        self.translation_key = f"{sensor_entry.station.code.lower()}_station_state"
        self._attr_unique_id = (
            f"{sensor_entry.station.code}.{sensor_entry.plant.name}.station_state"
        )
        self._attr_device_info = SwissPollenDataCoordinator.device_info(plant)
        self._attr_options = [
            "online",
            "offline",
            "error",
        ]

    @property
    def native_value(self) -> StateType | str:
        if self.coordinator.data is None:
            return None
        state = self.coordinator.data.station_state(self._sensor_entry.station)
        return state.description

    @property
    def icon(self) -> str | None:
        """Return the icon based on the current sensor value."""
        value = self.native_value

        if value == "online":
            return "mdi:check-circle"
        if value == "offline":
            return "mdi:close-circle"
        else:
            return "mdi:alert-circle"


class SwissPollenVersionSensor(
    CoordinatorEntity[SwissPollenDataCoordinator], SensorEntity
):
    def __init__(
        self,
        plant: Plant,
        coordinator: SwissPollenDataCoordinator,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = SensorEntityDescription(
            key=f"{plant.name}.remote.version",
            name="remote version",
            entity_category=EntityCategory.DIAGNOSTIC,
        )
        self._attr_has_entity_name = True
        self.translation_key = "backend_version"
        self._attr_unique_id = f"{plant.name}.backend_version"
        self._attr_device_info = SwissPollenDataCoordinator.device_info(plant)
        self._attr_icon = "mdi:label-outline"

    @property
    def native_value(self) -> StateType | str:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.backend_version()
