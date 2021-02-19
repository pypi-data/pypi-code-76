import os
import yaml
from typing import List, Optional
import sys
import site
import logging
from collections.abc import Mapping


logger = logging.getLogger(__name__)


class Settings:
    def __init__(self, filename: Optional[str] = None) -> None:
        super().__init__()
        self.defaults_filename = self.get_defaults_filename("pymdmix_core.yml")
        self.files = [self.defaults_filename]
        self.data: dict = self.load_data(self.defaults_filename)
        self.get = self.data.get
        self.home = os.path.dirname(self.defaults_filename)
        if filename is not None:
            self.update_settings_with_file(filename)

    def __getitem__(self, k):
        return self.data[k]

    def __len__(self):
        return len(self.data)

    def __contains__(self, k):
        return k in self.data

    def update_settings_with_file(self, filename: str):
        self.merge(self.load_data(filename))
        self.files.append(filename)

    def get_file(self, filename: str):
        return os.path.join(self.home, filename)

    @staticmethod
    def get_defaults_filename(filename: str) -> str:
        home_candidates = Settings.get_mdmix_homes()
        logger.info(f"Searching for mdmix home in: {home_candidates}")
        configs = [os.path.join(path, filename) for path in home_candidates]
        configs = [config for config in configs if os.path.exists(config)]
        if len(configs) > 0:
            logger.info(f"found configs: {configs}")
            config = configs[0]
            logger.info(f"Using {config} for default settings")
            return config
        else:
            logger.warning(f"no config file found in default locations for {filename}. trying current folder")
            return filename

    @staticmethod
    def get_mdmix_homes() -> List[str]:
        mdmix_home = os.getenv("MDMIX_HOME")
        paths = [sys.prefix, os.path.join(sys.prefix, "local")]
        paths += site.PREFIXES
        paths += ["/usr", "/usr/local"]
        paths = [os.path.join(path, "pymdmix") for path in paths]
        if mdmix_home is not None:
            paths = [mdmix_home] + paths
        return [path for path in paths if os.path.exists(path)]

    @staticmethod
    def load_data(filename: str) -> dict:
        with open(filename, "r") as file:
            d = yaml.load(file, Loader=yaml.FullLoader)
        return d if d is not None else {}

    def merge(self, data):
        def _merge(dict1, dict2):
            for key, value in dict2.items():
                if (
                    key in dict1
                    and isinstance(dict1[key], dict)
                    and isinstance(value, Mapping)
                ):
                    _merge(dict1[key], value)
                elif (
                    key in dict1
                    and isinstance(dict1[key], list)
                    and isinstance(value, list)
                ):
                    dict1[key] += value
                else:
                    dict1[key] = dict2[key]

        _merge(self.data, data)


SETTINGS = Settings()
