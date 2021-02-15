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

from typing import Any, List, Optional

from pydantic import Field

from kelvin.sdk.lib.common.models.apps.common import (
    DottedIdentifier,
    EnvironmentVar,
    Name,
    OPCUAEndpoint,
    PositiveNumber,
    PythonEntryPoint,
    Version,
    ZMQUrl,
)
from kelvin.sdk.lib.common.models.generic import KSDKModel
from kelvin.sdk.lib.common.models.types import BaseEnum
from kelvin.sdk.lib.common.utils.general_utils import standardize_string

try:
    from typing import Literal  # type: ignore
except ImportError:
    from typing_extensions import Literal  # type: ignore


class Images(KSDKModel):
    base: Optional[str] = Field(None, description="Base image.", title="Base Image")
    builder: Optional[str] = Field(None, description="Builder image.", title="Builder Image")


class ApplicationLanguage(BaseEnum):
    python = "python"  # default
    cpp = "cpp"

    def get_extension(self) -> str:
        return {ApplicationLanguage.python: ".py", ApplicationLanguage.cpp: ".cpp"}[self]

    def default_template(
        self,
        app_name: str,
        requirements: Optional[str] = None,
        makefile: Optional[str] = None,
        dso: Optional[str] = None,
    ) -> dict:
        from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs

        standard_app_name = standardize_string(app_name)
        if self == ApplicationLanguage.python:
            entrypoint = f"{standard_app_name}.{standard_app_name}:App"
            requirements = requirements or GeneralConfigs.default_requirements_file
            return {self.value_as_str: {"entry_point": entrypoint, "requirements": requirements}}
        if self == ApplicationLanguage.cpp:
            makefile = makefile or GeneralConfigs.default_makefile
            dso = dso or f"{standard_app_name}/{standard_app_name}.so"
            return {self.value_as_str: {"makefile": makefile, "dso": dso}}
        return {}


class CPPLanguageType(KSDKModel):
    dso: str = Field(..., description="Dynamic shared-object.", title="Dynamic Shared Object")
    makefile: Optional[str] = Field("CMakeLists.txt", description="Makefile.", title="Makefile")


class PythonLanguageType(KSDKModel):
    entry_point: PythonEntryPoint
    requirements: Optional[str] = Field("requirements.txt", description="Package requirements", title="Requirements")
    version: Optional[Literal["3.7", "3.8"]] = Field(None, description="Python version.", title="Python Version")


class ApplicationInterface(BaseEnum):
    client = "client"  # Default
    data = "data"

    @property
    def default_template(self) -> dict:
        value = {
            "period": 1.0,
        }
        if self == ApplicationInterface.data:
            value["timeout"] = 10.0

        return {self.value_as_str: value}


class ApplicationFlavour(BaseEnum):
    kelvin_app = "kelvin-app"  # Default
    core = "core"


class Language(KSDKModel):
    type: ApplicationLanguage = Field(..., description="Language type.", title="Language Type")
    python: Optional[PythonLanguageType] = None
    cpp: Optional[CPPLanguageType] = None


class InterfaceDescriptorType(BaseEnum):
    serial = "serial"
    ethernet = "ethernet"
    file = "file"


class ClientInterfaceType(KSDKModel):
    sub_url: Optional[ZMQUrl] = Field(
        None,
        title="Subscription URL",
        description="The URL for clients to connect to when subscribing to the core server",
    )
    pub_url: Optional[ZMQUrl] = Field(
        None,
        title="Publish URL",
        description="The URL for clients to connect to when publishing to the core server",
    )
    topic: Optional[str] = Field(
        "",
        title="Topic",
        description="Message topic to allow multiple clients to share the same pub/sub sockets.",
    )
    compress: bool = Field(False, title="Compress Data", description="If true, data is compressed")
    period: Optional[PositiveNumber] = Field(1.0, title="Polling Period", description="Polling period.")

    environment_vars: Optional[List[EnvironmentVar]] = Field(
        None,
        description="Environment variables. Non-strings will be json-encoded as strings.",
        title="Environment Variables",
    )
    executable: Optional[str] = Field(None, title="Executable Name", description="Executable name.")
    args: Optional[List[str]] = Field([], title="Executable Arguments", description="Executable arguments.")
    spawn: bool = Field(
        False,
        title="Spawn Executable",
        description="If true, core automatically spawns the executable at startup.",
    )
    dso: Optional[str] = Field(
        None,
        title="Dynamic Shared Object for Core RPC App",
        description="Dynamic shared-object for Core RPC app.",
    )


class DataInterfaceType(KSDKModel):
    period: PositiveNumber = Field(..., description="Polling period.", title="Polling Period")
    timeout: Optional[PositiveNumber] = Field(10, description="Timeout period.", title="Timeout Period")


class PollerInterfaceType(KSDKModel):
    period: PositiveNumber = Field(..., description="Polling period.", title="Polling Period")


class DataModel(KSDKModel):
    name: DottedIdentifier = Field(..., description="Data model name.", title="Data Model Name")
    version: Version = Field(..., description="Data model version.", title="Data Model Version")
    path: Optional[str] = Field(None, description="Data model path.", title="Data Model Path")


class Interface(KSDKModel):
    type: ApplicationInterface = Field(..., description="Interface type.", title="Interface Type")
    client: Optional[ClientInterfaceType] = None
    data: Optional[DataInterfaceType] = None


class Item(KSDKModel):
    name: DottedIdentifier = Field(..., description="Item name.", title="Item name")
    value: Any = Field(..., description="Item value.", title="Item value")


class IO(KSDKModel):
    name: DottedIdentifier = Field(..., description="Input/Output name.", title="Input/Output name")
    data_model: DottedIdentifier = Field(None, description="Data model name.", title="Data Model Name")
    values: List[Item] = []


class RegistryMapIO(KSDKModel):
    historize: bool = False
    upload: bool = False
    name: DottedIdentifier
    node: str
    external_tag: Optional[str] = None
    access: Literal["RO", "RW"] = "RW"


class RegistryMap(KSDKModel):
    inputs: List[RegistryMapIO] = []
    outputs: List[RegistryMapIO] = []
    parameters: List[RegistryMapIO] = []


class ConnectionType(BaseEnum):
    opcua = "opcua"


class OPCUAConnectionType(KSDKModel):
    registry_map: RegistryMap
    endpoint: OPCUAEndpoint


class Connection(KSDKModel):
    name: Name = Field(..., description="Connection name.", title="Connection name")
    type: ConnectionType = Field(ConnectionType.opcua, description="Connection type.", title="Connection type")
    opcua: OPCUAConnectionType


# required by migration command
class RunTime(KSDKModel):
    historize_inputs: bool = False
    historize_outputs: bool = True
    type: str = "opcua"


class Core(KSDKModel):
    version: Version = Field(..., description="Core version.", title="Core Version")
    language: Language
    interface: Interface
    # required by injector & extractor
    data_models: List[DataModel] = []
    runtime: RunTime = Field(
        description="Runtime configuration.", title="Runtime configuration", default_factory=RunTime
    )
    connections: List[Connection] = []
    inputs: List[IO] = []
    outputs: List[IO] = []
    configuration: List[IO] = []
    parameters: List[IO] = []


class KelvinAppType(KSDKModel):
    core: Core
    images: Optional[Images] = None
    system_packages: Optional[List[str]] = Field(None, description="System packages.", title="System packages")
