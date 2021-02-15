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
from typing import Optional, Sequence

import click

from kelvin.sdk.lib.common.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.common.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def secrets() -> bool:
    """
    Manage platform 'secrets'.
    """


@secrets.command(cls=KSDKCommand)
@click.argument("secret_name", nargs=1, type=click.STRING)
@click.option("--value", type=click.STRING, required=True, help=KSDKHelpMessages.secret_create_value)
def create(secret_name: str, value: str) -> bool:
    """
    Create a secret on the platform.

    """
    from kelvin.sdk.interface import secrets_create

    return secrets_create(secret_name=secret_name, value=value)


@secrets.command(cls=KSDKCommand)
@click.option("query", "--filter", type=click.STRING, required=False, help=KSDKHelpMessages.secret_list_filter)
def list(query: Optional[str]) -> bool:
    """
    List all the available secrets on the platform.

    """
    from kelvin.sdk.interface import secrets_list

    return bool(secrets_list(query=query, should_display=True))


@secrets.command(cls=KSDKCommand)
@click.argument("secret_names", nargs=-1, required=True, type=click.STRING)
def delete(secret_names: Sequence[str]) -> bool:
    """
    Delete secrets on the platform.

    """
    from kelvin.sdk.interface import secrets_delete

    return secrets_delete(secret_names=secret_names)
