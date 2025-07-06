from typing import Dict, List
from swiss_pollen import PollenService, Station, Measurement, Plant
from dataclasses import dataclass


@dataclass
class CurrentPollen:
    measurements: Dict[str, Measurement]
    stations: List[Station]
    active: bool


class PollenClient(object):
    def get_current_pollen_for_plant(
        self, plant: Plant, station_codes: list[str]
    ) -> CurrentPollen:
        result = {}
        pollen_data = PollenService.current_values(plants=[plant])
        active = False
        for station in pollen_data.keys():
            for measurement in pollen_data.get(station):
                if measurement.value > 0:
                    active = True
                if station.code in station_codes:
                    result[f"{station.code}-{measurement.plant.name}"] = measurement
        return CurrentPollen(result, pollen_data.keys(), active)
