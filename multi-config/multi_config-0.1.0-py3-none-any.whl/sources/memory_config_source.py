from ..configuration_source import IConfigurationSource
from typing import *

__all__ = [
    'MemoryConfigurationSource'
]


class MemoryConfigurationSource(IConfigurationSource):
    def __init__(self, values: dict = None):
        self._values = values or {}

    def add(self, key: str, value: Any) -> 'MemoryConfigurationSource':
        self._values[key] = value
        return self

    def get_value(self) -> dict:
        return self._values
