"""Kelvin-Core Client Configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterator, Mapping

import yaml
from pydantic import AnyUrl, BaseSettings, Field, ValidationError, validator
from pydantic.tools import parse_obj_as

from kelvin.icd import Model

from ..mapping_proxy import MappingProxy


class CoreClientConfig(BaseSettings, Model):
    """Kelvin-Core Client Configuration."""

    class Config(BaseSettings.Config, Model.Config):
        """Pydantic configuration."""

        env_prefix = "KELVIN_APP_CLIENT__"

    sub_url: AnyUrl = Field(
        "tcp://127.0.0.1:10411",
        title="Kelvin-Core Subscription URI",
        description="Kelvin-Core URI. e.g. tcp://127.0.0.1:12345",
    )
    pub_url: AnyUrl = Field(
        "tcp://127.0.0.1:21813",
        title="Kelvin-Core Publish URI",
        description="Kelvin-Core URI. e.g. tcp://127.0.0.1:54321",
    )
    period: float = Field(1.0, title="Polling Period", description="Polling period in seconds.")
    topic: str = Field("", title="Topic", description="Subscription topic.")
    compress: bool = Field(
        False, title="Compress messages", description="Use compression when encoding messages."
    )

    sync: bool = Field(
        True, title="Default Connection", description="Default connection type: sync/async"
    )

    @validator("configuration", always=True, pre=True)
    def validate_app_config(cls, value: Any, values: Dict[str, Any]) -> Any:
        """Validate app configuration field."""

        if isinstance(value, str):
            value = Path(value.strip()).expanduser().resolve()
            if not value.is_file():
                raise ValueError(f"Invalid file: {value}")

        if isinstance(value, Mapping):
            core_client_config = value
        elif isinstance(value, Path):
            value = yaml.safe_load(value.read_text())
            core_client_config = MappingProxy(value).get("app.kelvin.core.interface.client", {})
        else:
            return value

        for k, v in core_client_config.items():
            if v is None:
                continue
            f = cls.__fields__.get(k)
            if f is None:
                continue
            try:
                values[k] = parse_obj_as(f.type_, v)
            except ValidationError as e:
                e.args[0][0]._loc = (k,)
                raise e from None

        return value

    configuration: Dict[str, Any] = Field({}, title="Application Configuration")

    def __iter__(self) -> Iterator[str]:  # type: ignore
        """Key iterator."""

        return iter(self.__dict__)
