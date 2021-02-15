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

from typing import Any, Dict, List, Optional, Union

from pydantic import Extra, validator

from kelvin.sdk.lib.common.models.apps.common import OPCUAEndpoint
from kelvin.sdk.lib.common.models.generic import KSDKModel


class LegacyAppSDKInfo(KSDKModel):
    sdk_version: str
    base_image: Optional[str] = None
    data_model_builder_image: Optional[str] = None

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class LegacyAppInfo(KSDKModel):
    name: str
    title: str
    description: str
    version: str
    platform: Optional[str]
    type: str
    entry_point: str

    @property
    def docker_image_name(self) -> str:
        return f"{self.name}:{self.version}"


class LegacyAppResources(KSDKModel):
    memory: str
    cpu: Union[float, str]


class LegacyAppIO(KSDKModel):
    type: str


class LegacyAppThreshold(KSDKModel):
    title: str
    value: str
    type: str
    units: str
    default: str


class LegacyAppDescriptor(KSDKModel):
    type: str
    period: float
    timeout: Optional[float] = None

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        result = super().dict(*args, **kwargs)
        if result["timeout"] is None:
            del result["timeout"]
        return result


class LegacyAppConfiguration(KSDKModel):
    class Config:
        extra = Extra.allow

    descriptor: LegacyAppDescriptor
    thresholds: Optional[Dict[str, LegacyAppThreshold]] = {}

    @validator("thresholds")
    def must_provide_thresholds(cls, v: Optional[Dict]) -> Dict:  # noqa
        return v if v is not None else {}


class LegacyAppGlobalConfiguration(KSDKModel):
    sdk: LegacyAppSDKInfo
    info: LegacyAppInfo
    resources: LegacyAppResources
    datamodels: Optional[List[str]]
    capabilities: Optional[List[str]]
    configuration: LegacyAppConfiguration
    inputs: Dict[str, LegacyAppIO] = {}
    outputs: Dict[str, LegacyAppIO] = {}

    @validator("datamodels", "capabilities", pre=True)
    def must_provide_list(cls, v: Optional[List]) -> List:  # noqa
        return v if v is not None else []

    @validator("inputs", "outputs", pre=True)
    def must_provide_input_output_entries(cls, v: Optional[Dict]) -> Dict:  # noqa
        return v if v is not None else {}


class BindingIO(KSDKModel):
    endpoint: OPCUAEndpoint
    source: str
    target: str


class BindingsConfiguration(KSDKModel):
    inputs: List[BindingIO]
    outputs: List[BindingIO]


class LegacyEnvironmentConfiguration(KSDKModel):
    bindings: BindingsConfiguration
