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

from pydantic import Field

from kelvin.sdk.lib.common.models.apps.bundle_app import BundleAppType
from kelvin.sdk.lib.common.models.apps.common import Name, Version
from kelvin.sdk.lib.common.models.apps.docker_app import DockerAppType
from kelvin.sdk.lib.common.models.apps.flow_app import FlowAppType
from kelvin.sdk.lib.common.models.apps.kelvin_app import KelvinAppType
from kelvin.sdk.lib.common.models.generic import KSDKModel
from kelvin.sdk.lib.common.models.types import BaseEnum


class Encoding(BaseEnum):
    utf_8 = "utf-8"
    ascii = "ascii"
    latin_1 = "latin_1"


class Info(KSDKModel):
    name: Name = Field(..., description="Application name.", title="Application name")
    version: Version = Field(..., description="Application version.", title="Application Version")
    title: str = Field(..., description="Application title.", title="Application title")
    description: str = Field(..., description="Application description.", title="Application description")

    @property
    def app_name_with_version(self) -> str:
        return f"{str(self.name)}:{str(self.version)}"


class AppType(BaseEnum):
    kelvin = "kelvin"
    bundle = "bundle"
    docker = "docker"
    flow = "flow"


class App(KSDKModel):
    type: AppType = Field(..., description="Application type.", title="Application Type")
    docker: Optional[DockerAppType] = None
    kelvin: Optional[KelvinAppType] = None
    bundle: Optional[BundleAppType] = None
    flow: Optional[FlowAppType] = None


class KelvinAppConfiguration(KSDKModel):
    spec_version: Version = Field(..., description="Specification version.", title="Specification Version")
    info: Info
    app: App
