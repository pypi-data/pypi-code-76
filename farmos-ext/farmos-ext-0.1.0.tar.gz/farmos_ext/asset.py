"""General FarmOS Asset."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Union

from farmos_ext.farmobj import FarmObj
from farmos_ext.term import Crop, Season


class Asset(FarmObj):

    def __init__(self, farm, keys):
        if 'resource' not in keys:
            super().__init__(farm, keys)
        elif 'resource' in keys and keys['resource'] == 'farm_asset':
            super().__init__(
                farm, farm.asset.get({'id': keys['id']})['list'][0])

    @property
    def id(self) -> Optional[int]:  # pylint: disable=invalid-name
        return self.attr('id', int)

    @property
    def type(self) -> str:
        return self.attr('type', str)

    @property
    def description(self) -> Dict:
        return self.attr('description', str)

    @property
    def archived(self) -> Union[datetime, None]:
        key = self.key('archived')
        if key and key != '0':
            return FarmObj.timestamp_to_datetime(self.key('archived'))
        else:
            return None

    @property
    def flags(self) -> List[str]:
        return self.attr('flags', list)

    @property
    def created(self) -> Union[datetime, None]:
        return FarmObj.timestamp_to_datetime(self.key('created'))

    @property
    def changed(self) -> Union[datetime, None]:
        return FarmObj.timestamp_to_datetime(self.key('changed'))

    @property
    def uid(self) -> Union[int, None]:
        return int(self.key('uid')) if self.key('uid') else None

    @property
    def data(self) -> str:
        return self.attr('data', str)


class Planting(Asset):

    @property
    def crop(self) -> List[Crop]:
        return self.farm.terms(self.key('crop'), Crop)

    @property
    def season(self):
        return self.farm.terms(self.key('season'), Season)


class Animal(Asset):

    @property
    def animal_type(self) -> str:
        return self.attr('animal_type', str)

    @property
    def nicknames(self) -> List[str]:
        return self.attr('animal_nicknames', list)

    @property
    def castrated(self) -> bool:
        return self.attr('animal_castrated', bool)

    @property
    def sex(self) -> str:
        return self.attr('animal_sex', str)

    @property
    def tag(self):
        return self.attr('tag', str)

    @property
    def parent(self) -> List[Animal]:
        return self.farm.assets(self.key('parent'), Animal)

    @property
    def birth_date(self) -> Union[datetime, None]:
        return FarmObj.timestamp_to_datetime(self.key('date'))


class Equipment(Asset):

    @property
    def manufacturer(self) -> str:
        return self.attr('manufacturer', str)

    @property
    def model(self) -> str:
        return self.attr('model', str)

    @property
    def serial_number(self) -> str:
        return self.attr('serial_number', str)


class Sensor(Asset):
    pass


class Compost(Asset):
    pass
