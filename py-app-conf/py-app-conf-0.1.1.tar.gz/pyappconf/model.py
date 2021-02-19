from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import Optional, Union, Dict, Any, Callable

from pydantic import BaseSettings, validator, BaseModel
import yaml
import toml
import json
import appdirs


def _output_if_necessary(content: str, out_path: Optional[Union[str, Path]] = None):
    if out_path is not None:
        out_path = Path(out_path)
        out_path.write_text(content)


def _get_data_kwargs(**kwargs):
    default_kwargs = dict(
        exclude={"settings"},
    )
    if "exclude" in kwargs:
        default_kwargs["exclude"].update(kwargs["exclude"])
    kwargs.update(default_kwargs)
    return kwargs


class ConfigFormats(str, Enum):
    YAML = 'yaml'
    JSON = 'json'
    TOML = 'toml'


class AppConfig(BaseModel):
    app_name: str
    config_name: str = "config"
    custom_config_path: Optional[Path] = None
    default_format: ConfigFormats = ConfigFormats.TOML

    @property
    def config_base_location(self) -> Path:
        if self.custom_config_path is not None:
            return self.custom_config_path
        return Path(appdirs.user_config_dir(self.app_name)) / self.config_name

    @property
    def config_location(self) -> Path:
        return Path(str(self.config_base_location) + '.' + self.default_format.value)


class BaseConfig(BaseSettings):
    _settings: AppConfig
    settings: AppConfig = None  # type: ignore

    @validator('settings')
    def set_settings_from_class_if_none(cls, v):
        if v is None:
            return cls._settings
        return v

    def get_serializer(self) -> Callable[[Optional[Union[str, Path]], Optional[Dict[str, Any]]], str]:
        if self.settings.default_format == ConfigFormats.TOML:
            return self.to_toml
        if self.settings.default_format == ConfigFormats.YAML:
            return self.to_yaml
        if self.settings.default_format == ConfigFormats.JSON:
            return self.to_json
        raise NotImplementedError(f'unsupported format {self.settings.default_format}')

    @classmethod
    def get_deserializer(cls) -> Callable[[Union[str, Path]], 'BaseConfig']:
        if cls._settings.default_format == ConfigFormats.TOML:
            return cls.parse_toml
        if cls._settings.default_format == ConfigFormats.YAML:
            return cls.parse_yaml
        if cls._settings.default_format == ConfigFormats.JSON:
            return cls.parse_json
        raise NotImplementedError(f'unsupported format {cls._settings.default_format}')

    def save(self, serializer_kwargs: Optional[Dict[str, Any]] = None, **kwargs):
        if not self.settings.config_location.parent.exists():
            self.settings.config_location.parent.mkdir()
        self.get_serializer()(self.settings.config_location, serializer_kwargs, **kwargs)  # type: ignore

    @classmethod
    def load(cls) -> 'BaseConfig':
        return cls.get_deserializer()(cls._settings.config_location)

    @classmethod
    def _get_env_values(cls) -> Dict[str, Any]:
        env_file = getattr(cls.Config, 'env_file', None)
        return cls._build_environ(cls, _env_file=env_file)  # type: ignore

    def to_yaml(
        self,
        out_path: Optional[Union[str, Path]] = None,
        yaml_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        if yaml_kwargs is None:
            yaml_kwargs = {}
        kwargs = _get_data_kwargs(**kwargs)
        data = self.dict(**kwargs)
        yaml_str = yaml.safe_dump(data, **yaml_kwargs)
        _output_if_necessary(yaml_str, out_path)
        return yaml_str

    @classmethod
    def parse_yaml(cls, in_path: Union[str, Path]) -> "BaseConfig":
        data = yaml.safe_load(Path(in_path).read_text())
        data.update(cls._get_env_values())
        return cls(**data)

    def to_toml(
        self,
        out_path: Optional[Union[str, Path]] = None,
        toml_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        if toml_kwargs is None:
            toml_kwargs = {}
        kwargs = _get_data_kwargs(**kwargs)
        data = self.dict(**kwargs)
        toml_str = toml.dumps(data, **toml_kwargs)  # type: ignore
        _output_if_necessary(toml_str, out_path)
        return toml_str

    @classmethod
    def parse_toml(cls, in_path: Union[str, Path]) -> "BaseConfig":
        data = toml.load(in_path)
        data.update(cls._get_env_values())
        return cls(**data)

    def to_json(
        self,
        out_path: Optional[Union[str, Path]] = None,
        json_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        if json_kwargs is None:
            json_kwargs = {}
        kwargs = _get_data_kwargs(**kwargs)
        data = self.dict(**kwargs)
        json_str = json.dumps(data, **json_kwargs)
        _output_if_necessary(json_str, out_path)
        return json_str

    @classmethod
    def parse_json(cls, in_path: Union[str, Path]) -> "BaseConfig":
        data = json.loads(Path(in_path).read_text())
        data.update(cls._get_env_values())
        return cls(**data)
