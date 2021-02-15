"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional

from pydantic import Field, ValidationError, validator

from kelvin.sdk.lib.common.configs.internal.auth_manager_configs import AuthManagerConfigs
from kelvin.sdk.lib.common.exceptions import MandatoryConfigurationsException
from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationLanguage
from kelvin.sdk.lib.common.models.generic import KPath, KSDKModel, KSDKSettings
from kelvin.sdk.lib.common.models.types import LogType, TableFormat
from kelvin.sdk.lib.common.utils.logger_utils import logger


class GenericMetadataEntry(KSDKModel):
    url: Optional[str] = None
    path: Optional[str] = None
    realm: Optional[str] = None
    port: Optional[str] = None
    client_id: Optional[str] = None


class DockerMetadataEntry(GenericMetadataEntry):
    @property
    def full_docker_registry_url(self) -> str:
        return f"{self.url}:{self.port}"


class SchemaMetadataEntry(GenericMetadataEntry):
    minimum_spec_version: str
    latest_spec_version: str


class SDKMetadataEntry(GenericMetadataEntry):
    ksdk_minimum_version: str
    ksdk_latest_version: str
    docker_minimum_version: Optional[str]
    base_image_python: str
    base_image_cpp: str
    base_data_model_builder_image: str
    launchpad: Dict[str, Any] = {}

    def get_docker_image_for_lang(self, app_lang: Optional[ApplicationLanguage] = None) -> str:
        if app_lang and app_lang == ApplicationLanguage.cpp:
            return self.base_image_cpp
        return self.base_image_python


class CompanyMetadata(KSDKModel):
    authentication: GenericMetadataEntry
    docker: DockerMetadataEntry
    documentation: GenericMetadataEntry
    sdk: SDKMetadataEntry
    kelvin_schema: SchemaMetadataEntry = Field(None, alias="schema")


class KelvinSDKEnvironmentVariables(KSDKSettings):
    ksdk_version_warning: bool = True
    ksdk_docker_image_version_warning: bool = True
    ksdk_verbose_mode: bool = False
    ksdk_output_type: str = LogType.KSDK.value_as_str
    ksdk_colored_logs: bool = True
    ksdk_shell: bool = False
    ksdk_debug: bool = False
    ksdk_table_format: TableFormat = TableFormat.psql

    class Config:
        fields = {
            "ksdk_version_warning": {
                "env": "KSDK_VERSION_WARNING",
                "description": "If outdated, KSDK will warn the user. If the minimum version is not respected, "
                "it will block any operation until upgrade.",
            },
            "ksdk_docker_image_version_warning": {
                "env": "KSDK_DOCKER_IMAGE_VERSION_WARNING",
                "description": "Will warn the user if the base docker image present on the `app.yaml` is deprecated.",
            },
            "ksdk_verbose_mode": {
                "env": "KSDK_VERBOSE_MODE",
                "description": "If set to True, will activate --verbose mode by default on every command.",
            },
            "ksdk_output_type": {
                "env": "KSDK_OUTPUT_TYPE",
                "description": "Sets the output type: KSDK, JSON or KEY_VALUE",
            },
            "ksdk_colored_logs": {
                "env": "KSDK_COLORED_LOGS",
                "description": "If disabled, all logs will be output in the default OS color, ready to be captured.",
            },
            "ksdk_shell": {
                "env": "KSDK_SHELL",
                "description": "Enable built-in command shell.",
            },
            "ksdk_debug": {
                "env": "KSDK_DEBUG",
                "description": "If enabled, display debug information for errors.",
            },
            "ksdk_table_format": {
                "env": "KSDK_TABLE_FORMAT",
                "description": 'Set the table format for all data display operations. Check "tabulate" pypi page.',
            },
        }

    @validator(
        "ksdk_version_warning",
        "ksdk_docker_image_version_warning",
        "ksdk_verbose_mode",
        "ksdk_colored_logs",
        "ksdk_debug",
        pre=True,
    )
    def invalid_value(cls, v: Any, field: Any) -> Any:  # noqa
        if v is None or v in ["True", "False", "1", "0", True, False, 1, 0]:
            return v
        return False

    @validator(
        "ksdk_output_type",
        pre=True,
    )
    def invalid_output_type_value(cls, v: Any) -> Any:  # noqa
        if v in LogType.as_list():
            return v
        return LogType.KSDK.value_as_str

    @validator(
        "ksdk_table_format",
        pre=True,
    )
    def invalid_table_format_value(cls, v: Any) -> TableFormat:  # noqa
        if isinstance(v, TableFormat):
            return v
        elif isinstance(v, str):
            return TableFormat(v)
        return TableFormat.psql

    @property
    def descriptions(self) -> dict:
        fields = KelvinSDKEnvironmentVariables.Config.fields
        for k, v in self.dict().items():
            fields[k]["current_value"] = v
        return fields

    @property
    def private_fields(self) -> list:
        return ["ksdk_debug"]

    def dict(self, *args: Any, **kwargs: Any) -> Mapping[str, Any]:  # type: ignore
        result = super().dict(*args, **kwargs)
        table_format = result["ksdk_table_format"]
        result["ksdk_table_format"] = table_format.value if isinstance(table_format, TableFormat) else table_format
        return result


class KelvinSDKConfiguration(KSDKSettings):
    last_metadata_refresh: float
    current_url: str
    current_user: str
    ksdk_current_version: str
    ksdk_minimum_version: str
    ksdk_latest_version: str
    configurations: KelvinSDKEnvironmentVariables = KelvinSDKEnvironmentVariables()

    @validator(
        "configurations",
        pre=True,
    )
    def validate_configurations(cls, v: Any) -> KelvinSDKEnvironmentVariables:  # noqa
        return v if v is not None else KelvinSDKEnvironmentVariables()

    @property
    def versions(self) -> dict:
        return {
            "current_version": self.ksdk_current_version,
            "minimum_version": self.ksdk_minimum_version,
            "latest_version": self.ksdk_latest_version,
        }

    def reset(self) -> Any:
        self.current_url = ""
        self.current_user = ""
        return self


class KelvinSDKGlobalConfiguration(KSDKModel):
    kelvin_sdk_client_config_file_path: KPath
    ksdk_config_file_path: KPath
    kelvin_sdk: KelvinSDKConfiguration

    def commit_ksdk_configuration(self) -> KelvinSDKGlobalConfiguration:
        self.kelvin_sdk.to_file(path=self.ksdk_config_file_path)
        return self

    def reset_ksdk_configuration(self) -> Any:
        self.kelvin_sdk.reset()
        return self

    def get_metadata_for_url(self, url: Optional[str] = None) -> CompanyMetadata:
        if not url:
            url = self.kelvin_sdk.current_url
        if self.kelvin_sdk_client_config_file_path.exists():
            kelvin_sdk_client_config_dict = self.kelvin_sdk_client_config_file_path.read_yaml(verbose=False)
            kelvin_sdk_client_config = (
                kelvin_sdk_client_config_dict.get("client", {}).get("sites", {}).get(url, {}).get("metadata", {})
            )
            if kelvin_sdk_client_config:
                try:
                    return CompanyMetadata(**kelvin_sdk_client_config)
                except ValidationError as exc:
                    raise MandatoryConfigurationsException(exc)
        raise ValueError(AuthManagerConfigs.invalid_session_message)

    def set_configuration(self, config: str, value: Any) -> bool:
        if config:
            config = config.lower()
            if not self.kelvin_sdk.configurations:
                self.kelvin_sdk.configurations = KelvinSDKEnvironmentVariables()
            if config in self.kelvin_sdk.configurations.dict().keys():
                setattr(self.kelvin_sdk.configurations, config, value)
                logger.relevant(f'Successfully set "{config}" to "{value}"')
                self.commit_ksdk_configuration()
                return True
            logger.warning("The configuration you provided is invalid")
        else:
            logger.warning(f'Provided configuration "{config}" does not exist')
        return True

    def unset_configuration(self, config: str) -> bool:
        if config:
            config = config.lower()
            if not self.kelvin_sdk.configurations:
                self.kelvin_sdk.configurations = KelvinSDKEnvironmentVariables()
            if self.kelvin_sdk.configurations and config in self.kelvin_sdk.configurations.__dict__.keys():
                self.kelvin_sdk.configurations.__setattr__(config, None)
                logger.relevant(f'Successfully unset "{config}"')
                self.commit_ksdk_configuration()
        else:
            logger.warning(f'Provided configuration "{config}" does not exist')
        return True
