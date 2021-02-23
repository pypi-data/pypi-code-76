from typing import *

from .configuration_source import IConfigurationSource
from .configuration import Configuration

__all__ = [
    'ConfigurationBuilder'
]


class ConfigurationBuilder:
    def __init__(self):
        self._sources: Set[IConfigurationSource] = set()

    def add(self, source: IConfigurationSource) -> 'ConfigurationBuilder':
        self._sources.add(source)
        return self

    def build(self) -> Configuration:
        composite_values: Dict[str, Any] = dict()

        for source in self._sources:
            value = source.get_value()
            ConfigurationBuilder._merge(value, composite_values)

        return Configuration(**composite_values)

    @staticmethod
    def _merge(source: dict, destination: dict) -> None:
        for k, v in source.items():
            if isinstance(v, dict):
                ConfigurationBuilder._merge(v, destination.setdefault(k, {}))
            else:
                destination[k] = v
