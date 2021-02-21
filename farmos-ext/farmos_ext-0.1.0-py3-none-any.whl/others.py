
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Union

from farmos_ext.farmobj import FarmObj


class Measure(Enum):
    COUNT = 'count'
    LENGTH = 'length'
    AREA = 'area'
    VOLUME = 'volume'
    TIME = 'time'
    TEMPERATURE = 'temperature'
    VALUE = 'value'
    RATE = 'rate'
    RATING = 'rating'
    RATIO = 'ratio'
    PROBABILITY = 'probability'
    WEIGHT = 'weight'


@dataclass
class Quantity():
    measure: Measure
    label: str
    unit: str
    value: str

    def to_dict(self):
        return {
            "measure": self.measure.value,
            "unit": {
                'name': self.unit,
                "resource": "taxonomy_term"
            },
            "value": self.value,
            "label": self.label
        }


@dataclass
class Inventory():
    value: int
    asset_id: int

    def to_dict(self):
        return {
            "asset": {"id": self.asset_id},
            "value": str(self.value)
        }


class User(FarmObj):
    pass


class Content(FarmObj):

    @property
    def api_version(self) -> Union[str, None]:
        return self.key('api_version')

    @property
    def system_of_measurement(self) -> Union[str, None]:
        return self.key('system_of_measurement')

    @property
    def metrics(self) -> Dict:
        return self.key('metrics')

    @property
    def mapbox_api_key(self) -> str:
        return self.key('mapbox_api_key')

    @property
    def languages(self) -> Dict:
        return self.key('languages')

    @property
    def google_maps_api_key(self) -> str:
        return self.key('google_maps_api_key')

    @property
    def resources(self) -> Dict:
        return self.key('resources')


class Soil(FarmObj):
    pass
