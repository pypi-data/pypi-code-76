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

from typeguard import typechecked

from kelvin.sdk.lib.common.models.types import StatusDataSource
from kelvin.sdk.lib.common.utils.display_utils import DisplayObject


@typechecked
def acp_list(source: StatusDataSource = StatusDataSource.CACHE, should_display: bool = False) -> List[DisplayObject]:
    """
    Returns the list of acps available on the platform.

    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the ACPS available on the platform.

    """
    from kelvin.sdk.lib.common.api.acp import acp_list as _acp_list

    return _acp_list(source=source, should_display=should_display)


@typechecked
def acp_search(query: str, source: StatusDataSource, should_display: bool = False) -> List[DisplayObject]:
    """
    Search for acps matching the provided query.

    :param query: the query to search for.
    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the matching ACPs on the platform.

    """
    from kelvin.sdk.lib.common.api.acp import acp_list as _acp_list

    return _acp_list(query=query, source=source, should_display=should_display)


@typechecked
def acp_show(acp_name: str, source: StatusDataSource, should_display: bool = False) -> List[DisplayObject]:
    """
    Displays all the details of the specified acp from the platform.

    :param acp_name: the name of the acp.
    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the yielded ACP instance and its data.

    """
    from kelvin.sdk.lib.common.api.acp import acp_show as _acp_show

    return _acp_show(acp_name=acp_name, source=source, should_display=should_display)


@typechecked
def acp_provision_script() -> bool:
    """
    Get the provisioning script to apply on an ACP.

    :return: a boolean indicating the end of the ACP provision script retrieval.

    """
    from kelvin.sdk.lib.common.api.orchestration_provision import acp_provision_script as _acp_provision_script

    return _acp_provision_script()
