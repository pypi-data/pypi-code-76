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

from kelvin.sdk.lib.common.configs.internal.docker_configs import DockerConfigs
from kelvin.sdk.lib.common.docker.docker_manager import DockerManager
from kelvin.sdk.lib.common.models.factories.global_configurations_objects_factory import (
    get_docker_credentials_for_current_url,
    get_global_ksdk_configuration,
)
from kelvin.sdk.lib.common.models.ksdk_docker import KSDKDockerAuthentication, KSDKNetworkConfig


def get_default_ksdk_network_config() -> KSDKNetworkConfig:
    """
    Provide the default KSDKNetworkConfig object.
    This object contains the network and respective bridge to connect to.

    :return: a KSDKNetworkConfig object.

    """
    return KSDKNetworkConfig(
        network_name=DockerConfigs.default_ksdk_network, network_driver=DockerConfigs.default_ksdk_network_driver
    )


def get_docker_manager(
    credentials: Optional[KSDKDockerAuthentication] = None, network_configuration: Optional[KSDKNetworkConfig] = None
) -> DockerManager:
    minimum_docker_version: Optional[str]
    try:
        ksdk_global_configuration = get_global_ksdk_configuration()
        current_site_metadata = ksdk_global_configuration.get_metadata_for_url()
        minimum_docker_version = current_site_metadata.sdk.docker_minimum_version
    except Exception:
        minimum_docker_version = None

    credentials = credentials or get_docker_credentials_for_current_url()
    network_configuration = network_configuration or get_default_ksdk_network_config()

    return DockerManager(
        credentials=credentials,
        network_configuration=network_configuration,
        minimum_docker_version=minimum_docker_version,
    )
