import collections
from abc import abstractmethod
from typing import Dict, List, Optional


class ConfigKeyNoProviderException(Exception):
    def __init__(self, key: str):
        self.key = key
        super().__init__(f"Config key '{key}' not found in any config providers")


class ConfigProviderKeyNotFoundException(Exception):
    def __init__(self, key: str, provider_name: str):
        self.key = key
        self.provider_name = provider_name
        super().__init__(f"Config key '{key}' not found in '{provider_name}'")


class AbstractConfigProvider(object):
    @abstractmethod
    def get_priority(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_keys(self) -> list:
        raise NotImplementedError()

    @abstractmethod
    def get_value(self, key: str) -> str:
        raise NotImplementedError()


class DictConfigProvider(AbstractConfigProvider):
    def __init__(self, config_map: Dict[str, str], name: str, priority: int):
        self.config_map = config_map
        self.name = name
        self.priority = priority

    def get_priority(self) -> int:
        return self.priority

    def get_keys(self) -> list:
        return list(self.config_map.keys())

    def get_value(self, key: str) -> str:
        result: Optional[str] = self.config_map.get(key)
        if not result:
            raise ConfigProviderKeyNotFoundException(key, self.name)
        return result


class ConfigCollection(object):
    """
    Often referred to as "config" in the code
    """

    def __init__(self):
        self.providers = {}
        self.ordered_providers = []

    def add_provider(self, provider: AbstractConfigProvider):
        self.providers[provider.get_priority()] = provider
        self.ordered_providers = list(collections.OrderedDict(sorted(self.providers.items())).values())

    def get_keys(self) -> list:
        """
        Gets a list of keys
        :return: list
        """
        keys: List[str] = []
        for provider in self.ordered_providers:
            keys = keys + provider.get_keys()
        return keys

    def get(self, key: str, default: str = "") -> str:
        """
        Gets a key with a default
        :param key: str
        :param default: str
        :return: str
        """
        try:
            return self.get_or_fail(key)
        except ConfigKeyNoProviderException:
            return default

    def get_or_fail(self, key: str):
        provider: AbstractConfigProvider
        for provider in self.ordered_providers:
            if key in provider.get_keys():
                return provider.get_value(key)
        raise ConfigKeyNoProviderException(key)
