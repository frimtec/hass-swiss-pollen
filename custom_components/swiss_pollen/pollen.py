from typing import Dict, List
from swiss_pollen import (PollenService, Station, Measurement)
from dataclasses import dataclass

@dataclass
class CurrentPollen:
    measurements: Dict[str, Measurement]
    stations: List[Station]

class PollenClient(object):
    def get_current_pollen_for_all_stations(self) -> CurrentPollen:
        result = {}
        pollen_data = PollenService.current_values()
        for station in pollen_data.keys():
            for measurement in pollen_data.get(station):
                result[f"{station.code}-{measurement.plant.name}"] = measurement
        return CurrentPollen(result, pollen_data.keys())
