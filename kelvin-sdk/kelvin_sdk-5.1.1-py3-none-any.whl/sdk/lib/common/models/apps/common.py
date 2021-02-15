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

from typing import Optional

from pydantic import Field, PositiveFloat, PositiveInt, constr

from kelvin.sdk.lib.common.models.generic import KSDKModel


class DottedIdentifier(KSDKModel):
    __root__: constr(regex=r"^[a-zA-Z]\w*(\.[a-zA-Z]\w*)*$")  # type: ignore # noqa


class PythonEntryPoint(KSDKModel):
    __root__: constr(regex=r"^[a-zA-Z]\w*(\.[a-zA-Z]\w*)*:[a-zA-Z]\w*$")  # type: ignore # noqa


class Version(KSDKModel):
    __root__: str


class DockerImageRef(KSDKModel):
    __root__: constr(regex=r"^([^:]+(:\d+)?/)?[^:]+:[^:]+$")  # type: ignore # noqa


class Name(KSDKModel):
    __root__: constr(regex=r"^[a-zA-Z][a-zA-Z0-9-]*$")  # type: ignore # noqa


class Identifier(KSDKModel):
    __root__: constr(regex=r"^[a-zA-Z]\w*$")  # type: ignore # noqa


class CPU(KSDKModel):
    __root__: constr(regex=r"^[0-9](\.[0-9]+)?(m|)$")  # type: ignore  # noqa


class Port(KSDKModel):
    __root__: PositiveInt


class NonNegativeInteger(KSDKModel):
    __root__: int


class OPCUAEndpoint(KSDKModel):
    __root__: constr(regex=r"^opc\.tcp://.+$")  # type: ignore  # noqa


class MQTTURI(KSDKModel):
    __root__: constr(regex=r"^mqtts?://.+$")  # type: ignore  # noqa


class PositiveNumber(KSDKModel):
    __root__: PositiveFloat


class DockerImageName(KSDKModel):
    __root__: constr(regex=r"^([^:]+(:\d+)?/)?[^:]+")  # type: ignore  # noqa


class EnvironmentVar(KSDKModel):
    name: Identifier = Field(..., description="Environment variable name.", title="Environment Variable Name")
    value: Optional[str] = Field(None, description="Environment variable value.", title="Environment Variable Value")


class ZMQUrl(KSDKModel):
    __root__: constr(regex=r"^(tcp://[^:]+:[0-9]+|ipc://.+)$")  # type: ignore  # noqa
