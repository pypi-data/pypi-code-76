"""Main farm access."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, Iterable, Iterator, List, Type, Union

from farmos_ext.area import Area
from farmos_ext.asset import Asset, Equipment, Planting
from farmos_ext.log import (Activity, Birth, Harvest, Input, Log, Maintenance,
                            Medical, Observation, Purchase, Sale, Seeding,
                            SoilTest, Transplanting)
from farmos_ext.others import Content, Quantity
from farmos_ext.term import Crop, CropFamily, Season, Term, Unit
from farmOS import farmOS  # pylint: disable=wrong-import-order
from farmOS.client import BaseAPI  # pylint: disable=wrong-import-order


class FarmTypeMissingError(Exception):
    pass


def farm():
    """Access to farm with provided credentials."""
    return Farm()


class FileAPI(BaseAPI):

    def __init__(self, session):
        # Define 'log' as the farmOS API entity endpoint
        super().__init__(session=session, entity_type='file')


# pylint: disable=too-many-public-methods
class Farm(farmOS):

    def __init__(self, local_resources="./resources"):
        self._host = None
        self._user = None
        self._pass = None
        self.local_resources = local_resources

        if os.path.exists("farmos.cfg"):
            with open('farmos.cfg') as cfg:
                for line in cfg.readlines():
                    if line.startswith("HOST"):
                        self._host = line[line.index("=")+1:].strip()
                    if line.startswith("USER"):
                        self._user = line[line.index("=")+1:].strip()
                    if line.startswith("PASS"):
                        self._pass = line[line.index("=")+1:].strip()
            if not self._host:
                raise KeyError("HOST key is not defined in farmos.cfg")
            if not self._user:
                raise KeyError("USER key is not defined in farmos.cfg")
            if not self._pass:
                raise KeyError("PASS key is not defined in farmos.cfg")
            super().__init__(self._host)
            self._token = self.authorize(self._user, self._pass)
        else:
            raise Exception('farmos.cfg not found.')
        self.file = FileAPI(self.session)

    def assets(self,
               filters: Union[Dict, List[Dict], int, str] = None,
               asset_class: Type[Asset] = Asset) -> Iterator[Type[Asset]]:
        if isinstance(filters, list):
            for filt in filters:
                for asset in self.asset.get(filt)['list']:
                    yield asset_class(self, keys=asset)
        else:
            for asset in self.asset.get(filters)['list']:
                yield asset_class(self, keys=asset)

    # def _get_assets(self, items: List[Dict], obj_class):
    #     retitems = []
    #     for item in items:
    #         rets = self.asset.get(item['id'])
    #         if 'list' in rets:
    #             self.extract(rets, obj_class)
    #         else:
    #             retitems.append(obj_class(self, rets))
    #     return retitems

    def logs(self,
             filters: Union[Dict, List[Dict], int, str] = None,
             log_class: Type[Log] = Log) -> Iterator[Type[Log]]:
        if isinstance(filters, list):
            for filt in filters:
                for log in self.log.get(filt):
                    yield log_class(self, keys=log)
        elif isinstance(filters, int):
            yield log_class(self, keys=self.log.get(filters))
        else:
            for log in self.log.get(filters):
                yield log_class(self, keys=log)

    def terms(self, filters: Union[str, List[Dict], Dict] = None,
              term_class: Type[Term] = Term) -> Iterator[Type[Term]]:
        if isinstance(filters, list):
            for item in filters:
                for term in self.term.get({"tid": item['id']})['list']:
                    yield term_class(self, keys=term)
        else:
            rets = self.term.get(filters)
            yield term_class(self, keys=rets)

    def areas(self, filters: Union[Dict, List[Dict], int, str] = None) -> Iterator[Area]:
        if isinstance(filters, list):
            for filt in filters:
                for area in self.area.get(filt)['list']:
                    yield Area(self, keys=area)
        else:
            for area in self.area.get(filters)['list']:
                yield Area(self, keys=area)

    def _create_log(self, name: str, date: datetime, category: str, fields: Dict, done=False):
        data = {
            "name": name,
            "timestamp": str(int(datetime.timestamp(date))),
            "log_category": [{
                "name": category
            }],
            "type": "farm_observation"
        }
        data.update(fields)
        if 'done' not in data:
            data['done'] = '1' if done else '0'
        ret = self.log.send(data)
        return ret

    @property
    def content(self) -> Content:
        return Content(self, keys=self.info())

    @property
    def seasons(self) -> Iterator[Season]:
        for season in self.term.get("farm_season")['list']:
            yield Season(self, season)

    @property
    def crop_families(self) -> Iterator[CropFamily]:
        for fam in self.term.get("farm_crop_families")['list']:
            yield CropFamily(self, keys=fam)

    @property
    def crops(self) -> Iterator[Crop]:
        for crop in self.term.get("farm_crops")['list']:
            yield Crop(self, crop)

    def equipment(self, filters: Dict = None) -> Iterable[Equipment]:
        if not filters:
            filters = {'type': 'equipment'}
        else:
            filters.update({'type': 'equipment'})
        return self.assets(filters, Equipment)

    def plantings(self, filters: Dict = None) -> Iterable[Planting]:
        if not filters:
            filters = {'type': 'planting'}
        else:
            filters.update({'type': 'planting'})
        return self.assets(filters, Planting)

    @property
    def units(self) -> Iterable[Unit]:
        for unit in self.term.get('farm_quantity_units')['list']:
            yield Unit(self, unit)

    def harvests(self, filters: Dict = None) -> Iterable[Harvest]:
        if 'farm_harvests' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_harvest'}
            else:
                filters.update({'type': 'farm_harvest'})
            return self.logs(filters, Harvest)
        else:
            raise FarmTypeMissingError("Harvest logs not supported.")

    def seedings(self, filters: Dict = None) -> Iterable[Seeding]:
        if 'farm_seedings' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_seeding'}
            else:
                filters.update({'type': 'farm_seeding'})
            return self.logs(filters, Seeding)
        else:
            raise FarmTypeMissingError("Seeding logs not supported.")

    def transplants(self, filters: Dict = None) -> Iterable[Transplanting]:
        if 'farm_transplanting' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_transplanting'}
            else:
                filters.update({'type': 'farm_transplanting'})
            return self.logs(filters, Transplanting)
        else:
            raise FarmTypeMissingError("Transplanting logs not supported.")

    def observations(self, filters: Dict = None) -> Iterable[Observation]:
        if 'farm_observation' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_observation'}
            else:
                filters.update({'type': 'farm_observation'})
            return self.logs(filters, Observation)
        else:
            raise FarmTypeMissingError("Observation logs not supported.")

    def maintenances(self, filters: Dict = None) -> Iterator[Maintenance]:
        if 'farm_maintenance' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_maintenance'}
            else:
                filters.update({'type': 'farm_maintenance'})
            return self.logs(filters, Maintenance)
        else:
            raise FarmTypeMissingError("Maintenance logs not supported.")

    def purchases(self, filters: Dict = None) -> Iterator[Purchase]:
        if 'farm_purchase' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_purchase'}
            else:
                filters.update({'type': 'farm_purchase'})
            return self.logs(filters, Purchase)
        else:
            raise FarmTypeMissingError("Purchase logs not supported.")

    def sales(self, filters: Dict = None) -> Iterator[Sale]:
        if 'farm_sale' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_sale'}
            else:
                filters.update({'type': 'farm_sale'})
            return self.logs(filters, Sale)
        else:
            raise FarmTypeMissingError("Sale logs not supported.")

    def births(self, filters: Dict = None) -> Iterator[Birth]:
        if 'farm_birth' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_birth'}
            else:
                filters.update({'type': 'farm_birth'})
            return self.logs(filters, Birth)
        else:
            raise FarmTypeMissingError("Birth logs not supported.")

    def inputs(self, filters: Dict = None) -> Iterator[Input]:
        if 'farm_input' in self.content.resources['input']:
            if not filters:
                filters = {'type': 'farm_input'}
            else:
                filters.update({'type': 'farm_input'})
            return self.logs(filters, Input)
        else:
            raise FarmTypeMissingError("Input logs not supported.")

    def soil_tests(self, filters: Dict = None) -> Iterator[SoilTest]:
        if 'farm_soil_test' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_soil_test'}
            else:
                filters.update({'type': 'farm_soil_test'})
            return self.logs(filters, SoilTest)
        else:
            raise FarmTypeMissingError("Soil test logs not supported.")

    def activities(self, filters: Dict = None) -> Iterator[Activity]:
        if 'farm_activity' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_activity'}
            else:
                filters.update({'type': 'farm_activity'})
            return self.logs(filters, Activity)
        else:
            raise FarmTypeMissingError("Activity logs not supported.")

    def medicals(self, filters: Dict = None) -> Iterator[Medical]:
        if 'farm_medical' in self.content.resources['log']:
            if not filters:
                filters = {'type': 'farm_medical'}
            else:
                filters.update({'type': 'farm_medical'})
            return self.logs(filters, Medical)
        else:
            raise FarmTypeMissingError("Medical logs are not supported.")

    def create_planting(self, crop: Crop, season: str, location: str) -> Planting:
        ret = self.asset.send({
            "name": "{} {} {}".format(season, location, crop.name),
            "type": "planting",
            "crop": [
                {
                    "id": crop.tid
                }
            ],
            "season": [{"name": season}]
        })
        plant = Planting(self, keys=ret)
        return plant

    def create_seeding(self, planting: Planting, location: Area, crop: Crop,
                       date: datetime, seeds: int, source=None, done=False) -> Seeding:
        name = "Seed {} {} {}".format(date.year, location.name, crop.name)
        fields = {
            "type": "farm_seeding",
            "asset": [
                {
                    "id": planting.id,
                    "resource": "taxonomy_term"
                }
            ],
            "seed_source": source,
            "movement": {
                "area": [
                    {
                        "id": location.tid,
                        "resource": "taxonomy_term"
                    }
                ]
            },
            "quantity": [
                {
                    "measure": "count",
                    "value": str(seeds),
                    "unit": {
                        'name': 'Seeds',
                        "resource": "taxonomy_term"
                    }
                }
            ]
        }
        ret = self._create_log(name, date, 'Plantings', fields, done=done)
        return Seeding(self, keys=ret)

    def create_transplant(self, planting: Planting, location: Area, date: datetime, fields=None, done=False):
        name = "Transplant {}".format(planting.name)
        data = {
            "type": "farm_transplanting",
            "movement": {
                "area": [
                    {
                        "id": location.tid,
                        "resource": "taxonomy_term"
                    }
                ]
            },
            "asset": [
                {
                    "id": planting.id,
                    "resource": "taxonomy_term"
                }
            ]
        }
        if fields:
            data.update(fields)
        ret = self._create_log(name, date, 'Plantings', data, done=done)
        return Transplanting(self, ret)

    def create_harvest(self, planting: Planting, date: datetime, quantities: List[Quantity], done=False):
        name = "Harvest {} {}".format(date.year, planting.crop[0]['name'])
        data = {
            "type": "farm_harvest",
            "asset": [{
                "id": planting.id,
                "resource": "taxonomy_term"
            }]
        }

        if quantities:
            data["quantity"] = []
            for quantity in quantities:
                data["quantity"].append(quantity.to_dict())

        ret = self._create_log(name, date, 'Plantings', data, done=done)
        return Harvest(self, ret)

    def create_log(self, name: str, date: datetime, category: str, fields: Dict, done=False):
        return Log(self, self._create_log(name, date, category, fields, done))
