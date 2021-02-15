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


from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import Field

from kelvin.sdk.lib.common.models.generic import KSDKModel
from kelvin.sdk.lib.common.models.types import BaseEnum


class KSDKNetworkConfig(KSDKModel):
    network_name: str
    network_driver: str


class KSDKDockerAuthentication(KSDKModel):
    registry_url: str
    registry_port: str
    username: str
    password: str

    @property
    def full_registry_url(self) -> str:
        return f"{self.registry_url}:{self.registry_port}"


class DockerPort(KSDKModel):
    port_type: str = Field(None, alias="Type")
    private_port: str = Field(None, alias="PrivatePort")
    public_port: str = Field(None, alias="PublicPort")

    @property
    def port_mapping(self) -> str:
        return f"{self.port_type}:{self.private_port}->{self.public_port}"

    def __repr__(self) -> str:
        return self.port_mapping


class DockerContainer(KSDKModel):
    id: str
    container_names: Optional[List[str]]
    image_name: str
    running: bool = False
    id_address: Optional[str]
    ports: List[DockerPort] = []
    labels: Optional[dict] = {}


class DockerImage(KSDKModel):
    id: str
    parent_id: str
    tags: List[str]
    created: int
    labels: Optional[dict]

    @property
    def readable_created_date(self) -> str:
        value = datetime.fromtimestamp(self.created)
        return f"{value:%Y-%m-%d %H:%M:%S}"


class DockerImageNameDetails(KSDKModel):
    registry_url: str
    docker_image_name: str

    @property
    def repository_docker_image_name(self) -> str:
        image, version = self.image_name_and_version
        return f"{self.registry_url}/{image}:{version}"

    @property
    def exclude_registry(self) -> str:
        if "/" in self.docker_image_name:
            extra_url, docker_image = self.docker_image_name.rsplit("/", 1)
            self.docker_image_name = docker_image
        return self.docker_image_name

    @property
    def image_name_and_version(self) -> Tuple[str, str]:
        docker_image_name = self.exclude_registry
        if ":" in docker_image_name:
            image, version = docker_image_name.rsplit(":", 1)
        else:
            image, version = docker_image_name, "latest"

        return image, version

    @property
    def container_name(self) -> str:
        name, _ = self.image_name_and_version
        return f"{name}.app"


class DockerNetwork(KSDKModel):
    name: str = Field(None, alias="Name")
    id: str = Field(None, alias="Id")
    driver: str = Field(None, alias="Driver")
    created: str = Field(None, alias="Created")


class DockerBuildEntry(KSDKModel):
    stream: Optional[str]
    error: Optional[str] = None
    message: Optional[str] = None

    @property
    def stream_content(self) -> Optional[str]:
        return self.stream.strip() if self.stream and "\n" != self.stream else None

    @property
    def error_content(self) -> Optional[str]:
        return self.error.strip() if self.error and "\n" != self.error else None

    @property
    def message_content(self) -> Optional[str]:
        return self.message.strip() if self.message and "\n" != self.error else None

    @property
    def entry_has_errors(self) -> bool:
        has_error = self.error_content is not None or self.message_content is not None
        return has_error

    @property
    def log_content(self) -> str:
        stream_content = self.stream_content or ""
        error_content = self.error_content
        message_content = self.message_content
        stream_content += f"/{error_content}" if error_content else ""
        stream_content += f"/{message_content}" if message_content else ""
        return stream_content


class DockerProgressDetail(KSDKModel):
    current: Optional[int] = 0
    total: Optional[int] = 0


class DockerProgressStatus(BaseEnum):
    PULL_LAYER = "Pulling fs layer"
    DEFAULT = "Default"
    PREPARING = "Preparing"
    PUSHING = "Pushing"
    DOWNLOADING = "Downloading"


class DockerProgressEntry(KSDKModel):
    id: Optional[str]
    status: Optional[str]
    progress: Optional[str]
    progressDetail: Optional[DockerProgressDetail]  # noqa


class AppRunningContainers(KSDKModel):
    existing_images: List[DockerImage] = []
    existing_containers: List[DockerContainer] = []
