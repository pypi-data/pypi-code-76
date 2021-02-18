from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

import toml


class InvalidConfigException(Exception):
    pass


@dataclass
class MutableConfig:
    exclude: List[str] = None

    def dict(self):
        return asdict(self)


@dataclass
class Config(MutableConfig):
    line_length: int = 88


def load_config() -> Config:
    config_path = Path.cwd() / "pyproject.toml"
    if not config_path.exists():
        return Config()

    project_config = toml.load(config_path)
    tool_config = project_config.get("tool", {}).get("vgs-style", {})
    exclude = tool_config.get("exclude")
    if exclude:
        tool_config["exclude"] = exclude.split(",")

    try:
        user_config = MutableConfig(**tool_config)
    except TypeError as exc:
        raise InvalidConfigException(str(exc)) from exc

    return Config(**user_config.dict())
