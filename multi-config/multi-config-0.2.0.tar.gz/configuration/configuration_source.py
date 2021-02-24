from abc import ABC, abstractmethod

__all__ = [
    'IConfigurationSource'
]


class IConfigurationSource(ABC):

    @abstractmethod
    def get_value(self) -> dict:
        """Get the configuration values as a dictionary to feed into a configuration object"""
