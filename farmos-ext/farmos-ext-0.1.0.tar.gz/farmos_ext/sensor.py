

import json
import time
from datetime import datetime
from typing import Dict, List
import os

import requests

FULL_URL = "{0}{1}{2}"
SENSOR_URL = "farm/sensor/listener/"


class FarmSensorException(Exception):
    pass


class Sensor():

    def __init__(self, farm: str = None, pub: str = None, prv: str = None) -> None:
        if not pub:
            if os.environ.get("FARM_SENSOR_PUB_KEY"):
                self._public_key = os.environ.get("FARM_SENSOR_PUB_KEY")
            else:
                raise FarmSensorException("No Sensor Public Key found")
        else:
            self._public_key = pub

        if not prv:
            if os.environ.get("FARM_SENSOR_PRV_KEY"):
                self._private_key = os.environ.get("FARM_SENSOR_PRV_KEY")
        else:
            self._private_key = prv

        if not farm:
            if os.environ.get('FARM_SENSOR_HOST'):
                farm = os.environ.get('FARM_SENSOR_HOST')
            else:
                raise FarmSensorException("No Farm Host URL found")
        self._url = FULL_URL.format(farm, SENSOR_URL, self._public_key)

    def upload(self, data: Dict, sleep=True):
        requests.post(self._url, params={"private_key": self._private_key}, json=data)
        if sleep:
            countdown = "Upload delay ending in: {} seconds"
            for index in range(0, 70):
                print(countdown.format(70-index), end="\r")
                time.sleep(1)
            print(" " * len(countdown), end='\r')

    def get(self, name: str = None, start: datetime = None, end: datetime = None, limit: int = 0) -> List[Dict]:
        data = {}
        data['limit'] = limit
        if name:
            data['name'] = name
        if start:
            data['start'] = start.timestamp()
        if end:
            data['end'] = end.timestamp()
        if self._private_key:
            data['private_key'] = self._private_key
        req = requests.get(self._url, params=data)
        record = json.loads(req.text)
        return record

    def summary(self) -> Dict:
        return json.loads(requests.get("{}/summary".format(self._url), params={"private_key": self._private_key}).text)
