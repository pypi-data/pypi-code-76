from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

import toml


class InvalidConfigException(Exception):
    pass


@dataclass
class MutableConfig:
    exclude: List[str] = None
    application_import_names: List[str] = None

    def dict(self):
        return asdict(self)


@dataclass
class Config(MutableConfig):
    line_length: int = 88


def load_config() -> Config:
    config_path = Path.cwd() / 'pyproject.toml'
    if not config_path.exists():
        return Config()

    try:
        project_config = toml.load(config_path)
    except Exception as exc:
        raise InvalidConfigException(f'Invalid config: {exc}') from exc

    tool_config = project_config.get('tool', {}).get('vgs-style', {})
    try:
        user_config = MutableConfig(**tool_config)
    except TypeError as exc:
        raise InvalidConfigException(str(exc)) from exc

    return Config(**user_config.dict())
