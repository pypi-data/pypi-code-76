# Copyright 2019-2021 Cambridge Quantum Computing
#
# You may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
"""The config module defines a userspace pytket configuration."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Type, TypeVar
from uuid import UUID
from dataclasses import asdict
import json
import os


def get_config_file_path() -> Path:
    """Get a path to the config file on this machine."""
    config_dir: Path
    xdg_conifg_dir = os.environ.get("XDG_CONFIG_HOME")
    if xdg_conifg_dir is None:
        config_dir = Path.home() / ".config"
    else:
        config_dir = Path(xdg_conifg_dir)

    pytket_config_file = config_dir / "pytket" / "config.json"

    return pytket_config_file


def create_default_config(config_file_path: Path) -> None:
    """Create a config file and fill it with the default values."""
    config_file_path.parent.mkdir(parents=True, exist_ok=True)
    with config_file_path.open("w", encoding="utf-8") as config_file:
        config = {"enable_telemetry": None, "telemetry_id": None}
        json.dump(config, config_file, indent=2)


class PytketConfig:
    """PytketConfig represents a loaded telemetry config file."""

    enable_telemetry: bool
    telemetry_id: Optional[UUID]
    extensions: Dict[str, Any]

    def __init__(
        self,
        enable_telemetry: bool,
        telemetry_id: Optional[UUID],
        extensions: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.enable_telemetry = enable_telemetry
        self.telemetry_id = telemetry_id
        self.extensions = {} if extensions is None else extensions

    @classmethod
    def default(cls) -> "PytketConfig":
        """Construct a default PytketConfig"""
        return PytketConfig(enable_telemetry=False, telemetry_id=None)

    @classmethod
    def read_file(cls, config_file_path: Path) -> "PytketConfig":
        """Construct a PytketConfig from reading a file with a given Path."""
        with config_file_path.open("r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            return PytketConfig(
                config.get("enable_telemetry"),
                config.get("telemetry_id"),
                config.get("extensions"),
            )

    def write_file(self, config_file_path: Path) -> None:
        """Write a PytketConfig to a file with a given Path."""
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        with config_file_path.open("w", encoding="utf-8") as config_file:
            config = {
                "enable_telemetry": self.enable_telemetry,
                "telemetry_id": self.telemetry_id,
                "extensions": self.extensions,
            }
            json.dump(config, config_file, indent=2)


T_ext = TypeVar("T_ext", bound="PytketExtConfig")


class PytketExtConfig(ABC):
    @classmethod
    @abstractmethod
    def from_pytketconfig(cls: Type[T_ext], config: PytketConfig) -> T_ext:
        ...

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_ext_config(ext_config_type: Type[T_ext]) -> T_ext:
    return ext_config_type.from_pytketconfig(
        PytketConfig.read_file(get_config_file_path())
    )
