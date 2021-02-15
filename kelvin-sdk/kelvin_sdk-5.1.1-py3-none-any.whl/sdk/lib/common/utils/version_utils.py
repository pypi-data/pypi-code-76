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

from colorama import Fore

from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationLanguage
from kelvin.sdk.lib.common.models.types import VersionStatus

from .logger_utils import logger

color_formats = {
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "red": Fore.RED,
    "reset": Fore.RESET,
}


def assess_docker_image_version(current_docker_image: str, app_lang: ApplicationLanguage) -> bool:
    """
    Verifies whether the current docker image version is supported.

    Warn the user, if 'should_warn' is set to True, that the docker image is outdated.

    :param current_docker_image: the current version to check.
    :param app_lang: the minimum accepted version.

    :return: a boolean indicating whether the docker image is valid.

    """
    from kelvin.sdk.lib.common.models.factories.global_configurations_objects_factory import (
        get_global_ksdk_configuration,
    )

    ksdk_global_configuration = get_global_ksdk_configuration()
    current_site_metadata = ksdk_global_configuration.get_metadata_for_url()
    should_warn = ksdk_global_configuration.kelvin_sdk.configurations.ksdk_docker_image_version_warning
    pre_established_docker_image = current_site_metadata.sdk.get_docker_image_for_lang(app_lang=app_lang)

    version_status = assess_version_status(
        current_version=current_docker_image,
        minimum_version=current_docker_image,
        latest_version=pre_established_docker_image,
        should_warn=should_warn,
    )
    versions = {
        "minimum_version": current_docker_image,
        "current_version": current_docker_image,
        "latest_version": pre_established_docker_image,
    }
    display_args = {**color_formats, **versions}

    if version_status != VersionStatus.UP_TO_DATE:
        ksdk_docker_image_version_warning: str = """\n
                {red}The base image provided on "app.yaml" is outdated!{reset} \n
                {red}Current: {current_version}{reset} → {yellow}Latest: {latest_version}{reset} \n
                {yellow}Update your image to the latest version in your app configuration file.{yellow}
        """
        invalid_docker_image_warning = ksdk_docker_image_version_warning.format_map(display_args)
        logger.relevant(invalid_docker_image_warning)
        return False

    return True


def assess_version_status(
    current_version: str, minimum_version: str, latest_version: str, should_warn: bool = True
) -> VersionStatus:
    """
    Verifies whether the current KSDK version is supported.

    Warn the user, if 'should_warn' is set to True, that the SDK is outdated.
    Raise an exception should it not respect the minimum version.

    :param current_version: the current version to check.
    :param minimum_version: the minimum accepted version.
    :param latest_version: the latest version of the SDK.
    :param should_warn: if set to true, will warn the user in case the ksdk is out of version.

    :return: the corresponding version status.

    """
    try:

        from pkg_resources import parse_version

        current_v = parse_version(current_version)
        min_v = parse_version(minimum_version)
        latest_v = parse_version(latest_version)

        if (min_v <= current_v <= latest_v) or check_if_is_pre_release(version=current_version):
            if current_v < latest_v and should_warn:
                return VersionStatus.OUT_OF_DATE
        else:
            return VersionStatus.UNSUPPORTED
    except TypeError:
        pass
    return VersionStatus.UP_TO_DATE


def check_if_is_pre_release(version: str) -> bool:
    """
    :param version: the version to verify.

    :return: a bool indicating whether the version matches the indicated version type.

    """
    try:
        from pkg_resources.extern import packaging

        return packaging.version.Version(version).is_prerelease
    except Exception:
        return False
