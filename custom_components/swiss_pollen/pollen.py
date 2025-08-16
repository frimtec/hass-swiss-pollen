from swiss_pollen import PollenService, PollenResult, Plant, Station, Measurement, Level


class CurrentPollen:
    _pollen_result: PollenResult
    _plant: Plant

    def __init__(self, pollen_result: PollenResult, plant: Plant):
        self._pollen_result = pollen_result
        self._plant = plant

    def value_by_station(self, station: Station) -> int:
        measurement = self._pollen_result.measurement_by_station(station, self._plant)
        return measurement.value if measurement is not None else None

    def level_by_station(self, station: Station) -> Level:
        value = self.value_by_station(station)
        return Level.level(value).description if value is not None else None

    def station_by_code(self, station_code: str) -> Station:
        return self._pollen_result.station_by_code(station_code)

    def backend_version(self) -> str:
        return self._pollen_result.backend_version

    def is_plant_active(self):
        for station in self._pollen_result.current_values.keys():
            value_by_station = self.value_by_station(station)
            if value_by_station is not None and value_by_station > 0:
                return True
        return False


class PollenClient(object):
    def get_current_pollen_for_plant(self, plant: Plant) -> CurrentPollen:
        return CurrentPollen(PollenService.load(plants=[plant]), plant)
