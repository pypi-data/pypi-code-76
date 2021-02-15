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

from typing import List, Optional, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.responses import ACP, ACPMetrics, ACPStatus
from kelvin.sdk.lib.common.api.workload import retrieve_workload_and_workload_status_data
from kelvin.sdk.lib.common.auth.auth_manager import (
    login_client_on_current_url,
    retrieve_error_message_from_api_exception,
)
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs, GeneralMessages
from kelvin.sdk.lib.common.models.generic import GenericObject
from kelvin.sdk.lib.common.models.types import StatusDataSource
from kelvin.sdk.lib.common.utils.display_utils import (
    DisplayObject,
    display_data_entries,
    display_data_object,
    error_colored_message,
    success_colored_message,
    warning_colored_message,
)
from kelvin.sdk.lib.common.utils.general_utils import get_bytes_as_human_readable, get_datetime_as_human_readable
from kelvin.sdk.lib.common.utils.logger_utils import logger


def acp_list(
    query: Optional[str] = None, source: StatusDataSource = StatusDataSource.CACHE, should_display: bool = False
) -> List[DisplayObject]:
    """
    Returns the list of acps available on the platform.

    :param query: the query to search for.
    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the ACPS available on the platform.

    """
    try:
        acp_list_step_1 = "Retrieving ACPS.."
        if query:
            acp_list_step_1 = f'Searching ACPs that match "{query}"'

        logger.info(acp_list_step_1)

        display_obj = retrieve_acp_and_acp_status_data(query=query, source=source, should_display=should_display)

        return [display_obj]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error retrieving ACPs: {error_message}")

    except Exception as exc:
        logger.exception(f"Error retrieving ACPs: {str(exc)}")

    return []


def acp_show(
    acp_name: str, source: StatusDataSource = StatusDataSource.CACHE, should_display: bool = False
) -> List[DisplayObject]:
    """
    Displays all the details of the specified acp from the platform.

    :param acp_name: the name of the acp.
    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the yielded ACP instance and its data.

    """
    try:
        logger.info(f'Retrieving ACP details for "{acp_name}"')

        client = login_client_on_current_url()

        # 1 - Retrieve the ACP data
        acp_info: ACP = client.acp.get_acp(acp_name=acp_name)
        acp_info_display = display_data_object(
            data=acp_info, object_title=GeneralConfigs.table_title.format(title="ACP Info"), should_display=False
        )

        # 2 - If enabled, retrieve the ACP metrics
        acp_metrics_display_output: str = ""
        acp_metrics_data_display: Optional[DisplayObject] = None
        if acp_info.metrics_enabled:
            logger.info(f'ACP metrics available. Retrieving metrics for "{acp_name}"')
            acp_metrics_data = client.acp_metrics.get_acp_metrics(acp_name=acp_name)
            acp_metrics_data_display = retrieve_acp_metrics_data(acp_metrics_data=acp_metrics_data, title="ACP Metrics")
            acp_metrics_display_output = acp_metrics_data_display.tabulated_data

        # 3 - Retrieve the workload data corresponding to the ACP
        workloads_display = retrieve_workload_and_workload_status_data(
            acp_name=acp_name, source=source, should_display=False
        )
        acp_info_display_output = acp_info_display.tabulated_data

        workloads_display_output = workloads_display.tabulated_data

        if should_display:
            logger.info(f"{acp_info_display_output}\n{acp_metrics_display_output}\n{workloads_display_output}")

        return [item for item in [acp_info_display, acp_metrics_data_display, workloads_display] if item]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error showing ACP: {error_message}")

    except Exception as exc:
        logger.exception(f"Error showing ACP: {str(exc)}")

    return []


def retrieve_acp_metrics_data(acp_metrics_data: ACPMetrics, title: str = "") -> DisplayObject:
    """
    Unpack the data provided by the ACPMetrics object.

    :param acp_metrics_data: the ACPMetrics object.
    :param title: the title to associate to the the ACP metrics detail info.

    :return: a DisplayObject containing a simplified, pretty metrics object.
    """
    final_object: dict = {}

    allocation_data = acp_metrics_data.allocation
    cpu_utilization_data = acp_metrics_data.cpu_utilization
    disk_data = acp_metrics_data.disk
    memory_usage_data = acp_metrics_data.memory_usage
    network_data = acp_metrics_data.network

    if allocation_data:
        final_object["Allocation"] = {
            "CPU capacity": allocation_data.cpu_capacity,
            "CPU usage": allocation_data.cpu_requests,
            "Memory capacity": get_bytes_as_human_readable(input_bytes_data=allocation_data.memory_capacity),
            "Memory usage": get_bytes_as_human_readable(input_bytes_data=allocation_data.memory_requests),
        }

    if cpu_utilization_data:
        last_cpu_utilization_entry = cpu_utilization_data[-1] if cpu_utilization_data else None
        if last_cpu_utilization_entry:
            final_object["CPU utilization"] = {
                "Timestamp (date)": get_datetime_as_human_readable(input_date=last_cpu_utilization_entry.timestamp),
                "Value": last_cpu_utilization_entry.value,
            }

    if disk_data:
        final_object["Disk data"] = {
            "Total capacity": get_bytes_as_human_readable(input_bytes_data=disk_data.total_bytes),
            "Used capacity": get_bytes_as_human_readable(input_bytes_data=disk_data.used_bytes),
        }

    if memory_usage_data:
        last_memory_usage_entry = memory_usage_data[-1] if memory_usage_data else None
        if last_memory_usage_entry:
            final_object["Memory usage"] = {
                "Timestamp (date)": get_datetime_as_human_readable(input_date=last_memory_usage_entry.timestamp),
                "Value": get_bytes_as_human_readable(input_bytes_data=last_memory_usage_entry.value),
            }

    if network_data:
        final_object["Network data"] = {
            "Transmitted (Tx)": get_bytes_as_human_readable(input_bytes_data=network_data.total_tx),
            "Received (Rx)": get_bytes_as_human_readable(input_bytes_data=network_data.total_rx),
        }

    return display_data_object(data=final_object, object_title=title, should_display=False)


def retrieve_acp_and_acp_status_data(
    query: Optional[str] = None,
    source: StatusDataSource = StatusDataSource.CACHE,
    should_display: bool = True,
) -> DisplayObject:
    """
    Centralize all calls to acps.
    First, retrieve all acps that match the provided criteria.
    Second, retrieve all acps status.
    Last, merge both results and yield the result.

    :param query: the query to search specific acps.
    :param source: the acp status data source from where to obtain data.
    :param should_display: if specified, will display the results of this retrieve operation.

    :return: a DisplayObject containing the acps and respective status data.

    """
    client = login_client_on_current_url()

    acps = cast(List, client.acp.list_acp(search=query))
    acps_status = []

    if acps:
        acp_names_search_query = ",".join([acp.name for acp in acps])
        result = client.acp.list_acp_status(search=acp_names_search_query, source=source.value)
        acps_status = cast(List, result)

    data_to_display = _combine_acp_and_acp_status_data(acps=acps, acps_status=acps_status)

    return display_data_entries(
        data=data_to_display,
        header_names=["Name", "Title", "ACP Status", "Last seen"],
        attributes=["name", "title", "acp_status", "last_seen"],
        table_title=GeneralConfigs.table_title.format(title="ACPs"),
        should_display=should_display,
        no_data_message="No ACPs available",
    )


def _combine_acp_and_acp_status_data(acps: List[ACP], acps_status: List) -> List[GenericObject]:
    """
    When provided with a list of acps and a list of acp statuses, combined them into a list of compound objects.
    This list consists of a custom object that results from the merge of an acp and its status data.

    :param acps: the list of acps to combine.
    :param acps_status: the list of acp status objects to combine.

    :return: a list of GenericObjects.

    """
    acps = acps or []
    acps_status = acps_status or []
    data_to_display: List[GenericObject] = []
    default_status = _get_parsed_acp_status()
    for acp in acps:
        custom_object: dict = {
            "name": acp.name,
            "title": acp.title,
            "acp_status": default_status,
            "last_seen": default_status,
        }
        for status_entry in acps_status:
            if acp.name == status_entry.name and status_entry.status:
                acp_status = _get_parsed_acp_status(acp_status_item=status_entry.status)
                custom_object["acp_status"] = acp_status
                custom_object["last_seen"] = get_datetime_as_human_readable(input_date=status_entry.status.last_seen)
                break
        data_to_display.append(GenericObject(data=custom_object))

    return data_to_display


def _get_parsed_acp_status(acp_status_item: Optional[ACPStatus] = None) -> str:
    """
    When provided with an ACPStatus, yield the message the message with the provided color schema and format.

    :param acp_status_item: the ACPs status item containing all necessary information.

    :return: a formatted string with the correct color schema.

    """
    message = GeneralMessages.no_data_available
    state = GeneralMessages.no_data_available

    if acp_status_item:
        message = acp_status_item.message or message
        state = acp_status_item.state or state

    formatter_structure = {
        "connected": success_colored_message,
        "warning": warning_colored_message,
        "no_connection": error_colored_message,
    }
    formatter = formatter_structure.get(state)

    return formatter(message=message) if formatter else message
