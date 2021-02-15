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

from typing import List, Tuple

from typeguard import typechecked

from kelvin.sdk.lib.common.utils.display_utils import DisplayObject


@typechecked
def global_configurations_list(should_display: bool = False) -> List[DisplayObject]:
    """
    List all available configurations for KSDK

    :param should_display: specifies whether or not the display should output data.

    :return: the list of all available configurations and their current details.

    """
    from kelvin.sdk.lib.common.configs.global_configs_manager import (
        global_configurations_list as _global_configurations_list,
    )

    return _global_configurations_list(should_display=should_display)


@typechecked
def global_configurations_set(config: Tuple) -> bool:
    """
    Set the specified configuration on the platform system

    :param config: the configuration tuple that includes both the configuration and respective value.

    :return: a boolean indicating the configuration was successfully set.

    """
    from kelvin.sdk.lib.common.configs.global_configs_manager import (
        global_configurations_set as _global_configurations_set,
    )

    return _global_configurations_set(configuration=config)


@typechecked
def global_configurations_unset(config: str) -> bool:
    """
    Unset the specified configuration from the platform system

    :param config: the configuration to unset.

    :return: a boolean indicating the configuration was successfully set.

    """
    from kelvin.sdk.lib.common.configs.global_configs_manager import (
        global_configurations_unset as _global_configurations_unset,
    )

    return _global_configurations_unset(configuration=config)


@typechecked
def configurations_autocomplete(shell_type: str) -> bool:
    """
    Generate completion commands for shell.

    """

    from click._bashcomplete import get_completion_script

    print(get_completion_script("ksdk", "_KSDK_COMPLETE", shell_type))  # noqa

    return True


@typechecked
def pip_configure() -> bool:
    """
    A setup utility that shows how a pip configuration can be set

    """

    from kelvin.sdk.lib.common.configs.global_configs_manager import pip_configure as _pip_configure

    return _pip_configure()


@typechecked
def encode_string(value: str) -> str:
    """
    Return the url-encoded version of the provided string.

    Parameters
    ----------
    value : str
        the value to be url-encoded.

    Returns
    -------
    str
        the url-encoded value.


    """
    from kelvin.sdk.lib.common.configs.global_configs_manager import encode_string as _encode_string

    return _encode_string(value=value)
