import json
from ..configuration_source import IConfigurationSource


class JsonConfigurationSource(IConfigurationSource):
    def __init__(self, jsonpath: str):
        self._jsonpath = jsonpath

    def get_value(self) -> dict:
        with open(self._jsonpath, 'r') as f:
            value: dict = json.load(f)
            return value
