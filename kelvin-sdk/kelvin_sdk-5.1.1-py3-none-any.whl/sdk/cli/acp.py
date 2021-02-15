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
from typing import List

import click
from click import Choice

from kelvin.sdk.lib.common.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.common.models.types import StatusDataSource
from kelvin.sdk.lib.common.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def acp() -> bool:
    """
    Manage and view ACPs.

    """


@acp.command(cls=KSDKCommand)
@click.option("--source", type=Choice(StatusDataSource.as_list()), required=False, help=KSDKHelpMessages.status_source)
def list(source: str) -> List:
    """
    List all the available ACPs in the platform.

    """
    from kelvin.sdk.interface import acp_list

    return acp_list(source=StatusDataSource(source), should_display=True)


@acp.command(cls=KSDKCommand)
@click.argument("query", nargs=1, type=click.STRING)
@click.option("--source", type=Choice(StatusDataSource.as_list()), required=False, help=KSDKHelpMessages.status_source)
def search(query: str, source: str) -> List:
    """
    Search for specific ACPs based on a query.

    e.g. kelvin acp search "my-acp"
    """
    from kelvin.sdk.interface import acp_search

    return acp_search(query=query, source=StatusDataSource(source), should_display=True)


@acp.command(cls=KSDKCommand)
@click.argument("acp_name", nargs=1, type=click.STRING)
@click.option("--source", type=Choice(StatusDataSource.as_list()), required=False, help=KSDKHelpMessages.status_source)
def show(acp_name: str, source: str) -> List:
    """
    Show the details of an ACP.

    e.g. kelvin acp show "my-acp"
    """
    from kelvin.sdk.interface import acp_show

    return acp_show(acp_name=acp_name, source=StatusDataSource(source), should_display=True)


@acp.command(cls=KSDKCommand)
def provision_script() -> bool:
    """
    Add an ACP to the Kelvin platform in 2 easy steps.

    In a matter of minutes you can have your ACP up and running.

    """
    from kelvin.sdk.interface import acp_provision_script

    return acp_provision_script()
