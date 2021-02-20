from typing import List

from modular_message_bot.config.config_collection import AbstractConfigProvider, ConfigProviderKeyNotFoundException
from modular_message_bot.utils.common_utils import dir_exists, dir_files, file_contents


class SecretFilesProvider(AbstractConfigProvider):
    NAME = "Secret Files Config Provider"

    def __init__(self, priority: int, secret_dir: str = "/run/secrets"):
        self.secret_dir = secret_dir
        self.keys: List[str] = []
        self.keys_loaded = False
        self.priority = priority

    def get_priority(self) -> int:
        return self.priority

    def get_keys(self) -> List[str]:
        if not self.keys_loaded:
            self.keys_loaded = True
            if dir_exists(self.secret_dir):
                file: str
                for file in dir_files(self.secret_dir):
                    self.keys.append(file)
        return self.keys

    def get_value(self, key: str) -> str:
        if key not in self.get_keys():
            raise ConfigProviderKeyNotFoundException(key, self.NAME)
        file = f"{self.secret_dir}/{key}"
        return file_contents(file)
