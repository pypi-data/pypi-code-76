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

import click

from kelvin.sdk.lib.common.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.common.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def studio() -> bool:
    """
    Kelvin Studio integration that allows the modification of application configurations.
    """


@studio.command(cls=KSDKCommand)
@click.option(
    "--schema-file", "--schema", type=click.Path(exists=True), required=False, help=KSDKHelpMessages.studio_schema_file
)
@click.option(
    "--input-file", "--input", type=click.Path(exists=True), required=False, help=KSDKHelpMessages.studio_input_file
)
def start(schema_file: str, input_file: str) -> bool:
    """
    Start Kelvin Studio and configure an application.

    """
    from kelvin.sdk.interface import studio_start

    return studio_start(schema_file=schema_file, input_file=input_file)


@studio.command(cls=KSDKCommand)
def stop() -> bool:
    """
    Stop Kelvin Studio.

    """
    from kelvin.sdk.interface import studio_stop

    return studio_stop()
