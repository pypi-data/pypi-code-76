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


from typing import Tuple

import click
from click import Choice

from kelvin.sdk.lib.common.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.common.models.types import ShellType
from kelvin.sdk.lib.common.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def configuration() -> bool:
    """
    Local configurations that enhance the usage of this tool.

    """


@configuration.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all the available configurations for this tool.
    """
    from kelvin.sdk.interface import global_configurations_list

    return global_configurations_list(should_display=True) is not None


@configuration.command(cls=KSDKCommand)
@click.argument("config", type=click.STRING, nargs=2, required=True)
def set(config: Tuple) -> bool:
    """
    Set a local configuration for this tool.

    e.g. kelvin configuration set KSDK_VERBOSE_MODE True

    Configurations can also be set with environment variables:

    e.g (Unix) export KSDK_VERBOSE_MODE=1
    """
    from kelvin.sdk.interface import global_configurations_set

    return global_configurations_set(config=config)


@configuration.command(cls=KSDKCommand)
@click.argument("config", type=click.STRING, nargs=1, required=True)
def unset(config: str) -> bool:
    """
    Unset a local configuration for this tool.

    e.g. kelvin configuration unset KSDK_VERBOSE_MODE

    If the configuration is set as an environment variable, it can also be unset with:

    e.g (Unix) unset KSDK_VERBOSE_MODE
    """
    from kelvin.sdk.interface import global_configurations_unset

    return global_configurations_unset(config=config)


@configuration.command(cls=KSDKCommand, help=KSDKHelpMessages.autocomplete_message)
@click.option("--shell", type=Choice(ShellType.as_list()), required=True, help=KSDKHelpMessages.shell)
def autocomplete(shell: str) -> bool:
    """
    Generate completion commands for shell.

    """

    from kelvin.sdk.interface import configurations_autocomplete

    return configurations_autocomplete(shell_type=shell)


@configuration.group(cls=KSDKGroup)
def pip() -> bool:
    """
    Helper command to guide users with Python's pip configuration.

    """


@pip.command(cls=KSDKCommand)
@click.argument("value", type=click.STRING, nargs=1, required=True)
def encode(value: str) -> bool:
    """
    An helper command that allows users to encode a string.
    Suitable for password encoding.
    Recommendation: wrap the string in double quotes.

    e.g.: kelvin configuration pip encode 'my_value+/@'

    """

    from kelvin.sdk.interface import encode_string

    return bool(encode_string(value=value))


@pip.command(cls=KSDKCommand)
def configure() -> bool:
    """Displays the necessary steps to setup pip's configuration."""

    from kelvin.sdk.interface import pip_configure

    return pip_configure()
