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
from typing import Any, Dict, List, Optional

from pydantic import Field

from kelvin.sdk.lib.common.models.apps.common import DockerImageRef
from kelvin.sdk.lib.common.models.generic import KSDKModel


class Build(KSDKModel):
    dockerfile: Optional[str] = Field("Dockerfile", description="Docker file.", title="Docker File")
    context: Optional[str] = Field(".", description="Build context directory.", title="Build context")
    args: Optional[List[str]] = []


class DockerAppType(KSDKModel):
    image: Optional[DockerImageRef] = None
    entrypoint: Optional[List[str]] = None
    build: Optional[Build] = Field(None, description="Docker build configuration.", title="Build Configuration")
    configuration: Optional[Dict[str, Any]] = Field(
        None, description="Container Custom Configuration.", title="Container Custom Configuration"
    )
