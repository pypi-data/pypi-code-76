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

import time
from collections import Counter
from tempfile import NamedTemporaryFile
from textwrap import indent
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, cast

from tqdm import tqdm

from kelvin.sdk.client import Client
from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import WorkloadDeploy
from kelvin.sdk.client.model.responses import (
    ACP,
    App,
    Workload,
    WorkloadLogs,
    WorkloadMetrics,
    WorkloadStatus,
    WorkloadStatusItem,
)
from kelvin.sdk.lib.common.auth.auth_manager import (
    login_client_on_current_url,
    retrieve_error_message_from_api_exception,
)
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs, GeneralMessages
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.common.models.generic import GenericObject, KPath
from kelvin.sdk.lib.common.models.ksdk_workload_deployment import WorkloadDeploymentRequest, WorkloadTemplateData
from kelvin.sdk.lib.common.models.types import DelimiterStyle, StatusDataSource, WorkloadFileType
from kelvin.sdk.lib.common.schema.schema_manager import validate_app_schema_from_app_config_file
from kelvin.sdk.lib.common.utils.deploy_bulk_utils import load_workload_data, save_workload_data
from kelvin.sdk.lib.common.utils.display_utils import (
    DisplayObject,
    display_data_entries,
    display_data_object,
    display_yes_or_no_question,
    error_colored_message,
    success_colored_message,
    warning_colored_message,
)
from kelvin.sdk.lib.common.utils.general_utils import get_bytes_as_human_readable, get_datetime_as_human_readable
from kelvin.sdk.lib.common.utils.logger_utils import logger


def workload_list(
    query: Optional[str] = None,
    acp_name: Optional[str] = None,
    app_name: Optional[str] = None,
    app_version: Optional[str] = None,
    enabled: bool = True,
    source: StatusDataSource = StatusDataSource.CACHE,
    should_display: bool = False,
) -> List[DisplayObject]:
    """
    Returns the list of workloads filtered any of the arguments.

    :param query: the query to search for.
    :param acp_name: the name of the acp to filter the workloads.
    :param app_name: the name of the app to filter the workloads.
    :param app_version: the version of the acp to filter the workloads.
    :param enabled: indicates whether it should filter workloads by their status.
    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the workloads available on the platform.

    """
    try:
        workload_list_step_1 = "Retrieving workloads.."
        if query:
            workload_list_step_1 = f'Searching workloads that match "{query}"'

        logger.info(workload_list_step_1)

        display_obj = retrieve_workload_and_workload_status_data(
            query=query,
            app_name=app_name,
            acp_name=acp_name,
            app_version=app_version,
            enabled=enabled,
            source=source,
            should_display=should_display,
        )

        return [display_obj]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error retrieving workloads: {error_message}")

    except Exception as exc:
        logger.exception(f"Error retrieving workloads: {str(exc)}")

    return []


def workload_show(workload_name: str, source: StatusDataSource, should_display: bool = False) -> List[DisplayObject]:
    """
    Show the details of the specified workload.

    :param workload_name: the name of the workload.
    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: the Workload object matching the provided query.

    """
    try:
        workload_show_step_1 = f'Retrieving workload details for "{workload_name}"'
        base_table_title = GeneralConfigs.table_title.format(title="Workload Info")
        status_table_title = GeneralConfigs.table_title.format(title="Workload Status")
        metrics_table_title = GeneralConfigs.table_title.format(title="Workload Metrics")

        logger.info(workload_show_step_1)

        client = login_client_on_current_url()

        workload = client.workload.get_workload(workload_name=workload_name)
        workload_display = display_data_object(data=workload, should_display=False, object_title=base_table_title)

        workload_status = client.workload.get_workload_status(workload_name=workload_name, source=source.value)
        workload_status_display = display_data_object(
            data=workload_status, should_display=False, object_title=status_table_title
        )

        workload_metrics_display: Optional[DisplayObject]
        try:
            workload_metrics = client.workload.get_workload_metrics(workload_name=workload_name)
            workload_metrics_display = retrieve_workload_metrics_data(
                workload_metrics_data=workload_metrics, title=metrics_table_title
            )
        except APIError:
            workload_metrics_display = None

        # Display Workload
        base_info = workload_display.tabulated_data
        status_info = workload_status_display.tabulated_data

        if not workload_metrics_display:
            no_metrics = f'No workload metrics available for "{workload_name}"'
            metrics_info = warning_colored_message(message=no_metrics)
        else:
            metrics_info = workload_metrics_display.tabulated_data

        if should_display:
            logger.info(f"{base_info}\n{status_info}\n{metrics_info}")

        return [x for x in [workload_display, workload_status_display, workload_metrics_display] if x]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error showing workload: {error_message}")

    except Exception as exc:
        logger.exception(f"Error showing workload: {str(exc)}")

    return []


def workload_deploy(workload_deployment_request: WorkloadDeploymentRequest) -> bool:
    """
    Deploy a workload from the specified deploy request.

    :param workload_deployment_request: the deployment object that encapsulates all the necessary parameters for deploy.

    :return: a boolean indicating whether the workload deploy operation was successful.

    """
    try:
        logger.info("Creating workload..")

        # 0 - Load the app configuration and validate its contents against the schema.
        app_config_file_path: KPath = KPath(workload_deployment_request.app_config)
        validate_app_schema_from_app_config_file(app_config_file_path=app_config_file_path)

        client = login_client_on_current_url()

        # 1 - Load the app configuration app
        loaded_app_config_object = KPath(workload_deployment_request.app_config).read_yaml()
        if not workload_deployment_request.quiet and loaded_app_config_object:
            logger.info("Application configuration successfully loaded")

        workload_deploy_payload: WorkloadDeploy = WorkloadDeploy(
            acp_name=workload_deployment_request.acp_name,
            app_name=workload_deployment_request.app_name,
            app_version=workload_deployment_request.app_version,
            name=workload_deployment_request.workload_name,
            title=workload_deployment_request.workload_title or workload_deployment_request.workload_name,
            payload=loaded_app_config_object,
        )

        deploy_result = client.workload.deploy_workload(data=workload_deploy_payload)
        if not workload_deployment_request.quiet and deploy_result:
            success_message = f"""\n
                Workload "{deploy_result.name}" successfully deployed. 
        
                To check the workload logs run the following command:
                        kelvin workload logs {deploy_result.name}
        
                To update this workload run the following command:
                        kelvin workload update {deploy_result.name}
            """
            logger.relevant(success_message)

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error creating workload: {error_message}")

    except Exception as exc:
        logger.exception(f"Error creating workload: {str(exc)}")

    return False


def workload_update(
    workload_name: str, app_config: str, workload_title: Optional[str], app_version: Optional[str]
) -> bool:
    """
    Update an existing workload with the new parameters.

    :param workload_name: the name for the workload to update.
    :param app_config: the path to the app configuration file.
    :param app_version: the the version of the app.
    :param workload_title: the title for the  workload.

    :return: a boolean indicating whether the workload update operation was successful.

    """
    try:
        logger.info(f'Updating workload "{workload_name}"')

        client = login_client_on_current_url()

        workload: Workload = client.workload.get_workload(workload_name=workload_name)

        workload_deployment_request: WorkloadDeploymentRequest = WorkloadDeploymentRequest(
            acp_name=workload.acp_name,
            app_name=workload.app_name,
            app_version=app_version or workload.app_version,
            workload_name=workload.name,
            workload_title=workload_title or workload.title,
            app_config=app_config,
        )

        deploy_result = workload_deploy(workload_deployment_request=workload_deployment_request)

        if deploy_result:
            logger.relevant(f'Workload "{workload_name}" successfully updated')

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error updating workload: {error_message}")

    except Exception as exc:
        logger.exception(f"Error updating workload: {str(exc)}")

    return False


def workload_logs(workload_name: str, tail_lines: str, output_file: Optional[str], follow: bool) -> bool:
    """
    Show the logs of a deployed workload.

    :param workload_name: the name of the workload.
    :param tail_lines: the number of lines to retrieve on the logs request.
    :param output_file: the file to output the logs into.
    :param follow: a flag that indicates whether it should trail the logs, constantly requesting for more logs.

    :return: a boolean indicating the end of the workload show logs operation.

    """
    try:
        logger.info(f'Retrieving workload logs for "{workload_name}"')

        client = login_client_on_current_url()

        _retrieve_workload_logs(
            client=client,
            workload_name=workload_name,
            since_time=None,
            tail_lines=tail_lines,
            output_file=output_file,
            follow=follow,
        )

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error retrieving logs for workload: {error_message}")

    except Exception as exc:
        logger.exception(f"Error retrieving logs for workload: {str(exc)}")

    return False


def workload_undeploy(workload_name: str, ignore_destructive_warning: bool = False) -> bool:
    """
    Stop and delete a workload on the platform.

    :param workload_name: the name of the workload to be stopped and deleted.
    :param ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    :return: a boolean indicating the end of the workload deletion operation.

    """
    try:
        if not ignore_destructive_warning:
            workload_undeploy_confirmation: str = """
                This operation will remove the workload from the ACP.
                All workload local data will be lost.
            """
            ignore_destructive_warning = display_yes_or_no_question(workload_undeploy_confirmation)

        if ignore_destructive_warning:
            logger.info(f'Undeploying workload "{workload_name}"')

            client = login_client_on_current_url()

            client.workload.undeploy_workload(workload_name=workload_name)

            logger.relevant(f'Workload "{workload_name}" successfully undeployed')

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error undeploying workload: {error_message}")

    except Exception as exc:
        logger.exception(f"Error undeploying workload: {str(exc)}")

    return False


def workload_start(workload_name: str) -> bool:
    """
    Start the provided workload.

    :param workload_name: the workload to start on the platform.

    :return: a boolean indicating the end of the workload start operation.

    """
    try:
        logger.info(f'Starting workload "{workload_name}"')

        client = login_client_on_current_url()

        client.workload.start_workload(workload_name=workload_name)

        logger.relevant(f'Workload "{workload_name}" successfully started')

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error starting workload: {error_message}")

    except Exception as exc:
        logger.exception(f"Error starting workload: {str(exc)}")

    return False


def workload_stop(workload_name: str, ignore_destructive_warning: bool = False) -> bool:
    """
    Stop the provided workload.

    :param workload_name: the workload to stop on the platform.
    :param ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    :return: a boolean indicating the end of the workload stop operation.

    """
    try:
        if not ignore_destructive_warning:
            workload_stop_confirmation: str = """
                This operation will stop the workload from running in the ACP.
                The persistent data will be kept intact.
            """
            ignore_destructive_warning = display_yes_or_no_question(workload_stop_confirmation)

        if ignore_destructive_warning:
            logger.info(f'Stopping workload "{workload_name}"')

            client = login_client_on_current_url()

            client.workload.stop_workload(workload_name=workload_name)

            logger.relevant(f'Workload "{workload_name}" successfully stopped')

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error stopping workload: {error_message}")

    except Exception as exc:
        logger.exception(f"Error stopping workload: {str(exc)}")

    return False


def workload_deploy_bulk(
    filename: str,
    file_type: Optional[str],
    output_filename: Optional[str],
    ignore_failures: bool,
    skip_successes: bool,
    dry_run: bool,
) -> bool:
    """
    Deploy workloads for ACPs in bulk.

    :param filename: The filename to load the configurations from.
    :param file_type: The type of the workload file.
    :param output_filename: The output file into which the results will be written.
    :param ignore_failures: Ignore deployment failures and automatically continue.
    :param skip_successes: Skip previous successes.
    :param dry_run: Validate inputs only.

    :return: a boolean indicating whether or not the bulk deploy procedure was successful.

    """
    try:
        logger.info("Deploying configuration in bulk..")

        file = KPath(filename).expanduser().resolve()

        if not file.is_file():
            logger.error(f"File does not exist: {file}")
            return False

        _file_type = WorkloadFileType.parse_file_type(file_type=file_type, file=file)

        _workload_data = load_workload_data(file=file, file_type=_file_type, field_map=None)

        results, errors = _deploy_bulk_workload(
            workload_data=cast(Sequence, _workload_data),
            ignore_failures=ignore_failures,
            skip_successes=skip_successes,
            dry_run=dry_run,
        )

        save_workload_data(
            file=file, filename=filename, output_filename=output_filename, file_type=_file_type, results=results
        )

        successful = not errors
        if successful:
            logger.relevant("Bulk deployment operation concluded with success.")
        else:
            logger.warning("Bulk deployment operation incomplete. Please check operation logs.")
        return successful

    except APIError as exc:
        reason = retrieve_error_message_from_api_exception(api_error=exc)
        error_message = f"Error performing bulk deployment operation: {reason}"
        logger.error(error_message)

    except Exception as exc:
        error_message = f"Error performing bulk deployment operation: {exc}"
        logger.error(error_message)

    return False


def retrieve_workload_metrics_data(workload_metrics_data: WorkloadMetrics, title: str = "") -> DisplayObject:
    """
    Unpack the data provided by the WorkloadMetrics object.

    :param workload_metrics_data: the WorkloadMetrics object.
    :param title: the title to associate to the the ACP metrics detail info.

    :return: a DisplayObject containing a simplified, pretty metrics object.
    """
    final_object: dict = {}

    allocation_data = workload_metrics_data.allocation
    cpu_utilization_data = workload_metrics_data.cpu_utilization
    memory_usage_data = workload_metrics_data.memory_usage
    network_data = workload_metrics_data.network

    if allocation_data:
        final_object["Allocation"] = {
            "CPU usage": allocation_data.cpu_requests,
            "Memory usage": get_bytes_as_human_readable(input_bytes_data=allocation_data.memory_requests),
        }

    if cpu_utilization_data:
        last_cpu_utilization_entry = cpu_utilization_data[-1] if cpu_utilization_data else None
        if last_cpu_utilization_entry:
            final_object["CPU utilization"] = {
                "Timestamp (date)": get_datetime_as_human_readable(input_date=last_cpu_utilization_entry.timestamp),
                "Value": last_cpu_utilization_entry.value,
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


def retrieve_workload_and_workload_status_data(
    query: Optional[str] = None,
    app_name: Optional[str] = None,
    acp_name: Optional[str] = None,
    app_version: Optional[str] = None,
    enabled: Optional[bool] = None,
    source: StatusDataSource = StatusDataSource.CACHE,
    should_display: bool = True,
) -> DisplayObject:
    """
    Centralize all calls to workloads.
    First, retrieve all workloads that match the provided criteria.
    Second, retrieve all workload status.
    Last, merge both results and yield the result.

    :param acp_name: the name of the acp to filter the workloads.
    :param app_name: the name of the app to filter the workloads.
    :param app_version: the version of the acp to filter the workloads.
    :param enabled: indicates whether it should filter workloads by their status.
    :param query: the query to query specific workloads.
    :param source: the status data source from where to obtain data.
    :param should_display: if specified, will display the results of this retrieve operation.

    :return: a DisplayObject containing the workload and respective status data.

    """
    client = login_client_on_current_url()

    yielded_workloads = (
        cast(
            List,
            client.workload.list_workload(
                app_name=app_name,
                acp_name=acp_name,
                app_version=app_version,
                enabled=enabled,
                search=query,
            ),
        )
        or []
    )

    yielded_workload_status = []
    if yielded_workloads:
        workload_names_search_query = ",".join([workload.name for workload in yielded_workloads])
        result = client.workload.list_workload_status(search=workload_names_search_query, source=source.value)
        yielded_workload_status = cast(List, result) or []

    data_to_display = _combine_workload_and_workload_status_data(
        workloads=yielded_workloads, workloads_status=yielded_workload_status
    )

    return display_data_entries(
        data=data_to_display,
        header_names=[
            "Name",
            "Title",
            "ACP Name",
            "App Name",
            "App Version",
            "Workload Status",
            "Last Seen",
        ],
        attributes=[
            "name",
            "title",
            "acp_name",
            "app_name",
            "app_version",
            "workload_status",
            "last_seen",
        ],
        table_title=GeneralConfigs.table_title.format(title="Workloads"),
        should_display=should_display,
        no_data_message="No workloads available",
    )


def _combine_workload_and_workload_status_data(
    workloads: List[Workload], workloads_status: List[WorkloadStatus]
) -> List[GenericObject]:
    """
    When provided with a list of workloads and a list of workload status, retrieve the list of items to display.
    This list consists of custom objects that correspond to the merge of a workload and its workload status.

    :param workloads: the list of workloads to combine.
    :param workloads_status: the list containing the status for each existing workload.

    :return: a list of GenericObjects.

    """
    workloads = workloads or []
    workloads_status = workloads_status or []
    # defaults
    data_to_display: List[GenericObject] = []
    default_status = _get_parsed_workload_status()
    for workload in workloads:
        custom_object = workload.dict()
        custom_object["workload_status"] = default_status
        custom_object["last_seen"] = default_status
        for status_entry in workloads_status:
            if status_entry.name == workload.name and status_entry.status:
                workload_status = _get_parsed_workload_status(workload_status_item=status_entry.status)
                custom_object["workload_status"] = workload_status
                custom_object["last_seen"] = get_datetime_as_human_readable(input_date=status_entry.status.last_seen)
                break
        data_to_display.append(GenericObject(data=custom_object))

    return data_to_display


def _retrieve_workload_logs(
    client: Client,
    workload_name: str,
    since_time: Optional[str],
    tail_lines: Optional[str],
    output_file: Optional[str],
    follow: bool = False,
) -> bool:
    """
    :param client: the Kelvin SDK Client object used to retrieve data.
    :param workload_name: the name of the workload.
    :param tail_lines: the number of lines to retrieve on the logs request.
    :param output_file: the file to output the logs into.
    :param follow: a flag that indicates whether it should trail the logs, constantly requesting for more logs.

    :return: a boolean indicating the end of the internal workload logs retrieval operation.

    """
    logs_for_workload: WorkloadLogs = client.workload_logs.get_workload_logs(
        workload_name=workload_name, since_time=since_time, tail_lines=tail_lines
    )

    file_path = KPath(output_file) if output_file else None

    if logs_for_workload.logs:
        for key, value in logs_for_workload.logs.items():
            log_strings = [entry for entry in value if entry]
            last_date = _extract_last_date_from_log_entries(entry=log_strings)
            entry_logs = "\n".join(log_strings)
            logger.info(entry_logs)
            # output to file
            if file_path:
                file_path.write_text(entry_logs)
            # if it should follow, return the recursive call
            if follow:
                time.sleep(10)
                return _retrieve_workload_logs(
                    client=client,
                    workload_name=workload_name,
                    since_time=last_date,
                    tail_lines=tail_lines,
                    output_file=output_file,
                    follow=follow,
                )
            # finish with success
            elif not follow and file_path:
                logger.info(f'Workload logs successfully written to "{str(file_path)}"')
    else:
        logger.warning(f'No workload logs available for "{workload_name}"')
    return True


def _extract_last_date_from_log_entries(entry: List) -> Optional[str]:
    """
    Retrieves the latest date from the provided list of logs.

    :param entry: the log entries to retrieve the data from.

    :return: a string containing the parsed datetime.

    """
    if entry:
        import re

        last_entry = entry[-1]
        match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d\+Z", last_entry)
        if match:
            return match.group()
    return None


def _get_parsed_workload_status(workload_status_item: Optional[WorkloadStatusItem] = None) -> str:
    """
    When provided with a WorkloadStatusItem, yield the message the message with the provided color schema and format.

    :param workload_status_item: the Workload status item containing all necessary information.

    :return: a formatted string with the correct color schema.

    """
    message = GeneralMessages.no_data_available
    state = GeneralMessages.no_data_available

    if workload_status_item:
        message = workload_status_item.message or message
        state = workload_status_item.state or state

    formatter_structure = {
        "deploying": warning_colored_message,
        "running": success_colored_message,
        "failed": error_colored_message,
        "no_connection": error_colored_message,
    }
    formatter = formatter_structure.get(state)

    return formatter(message=message) if formatter else message


def _deploy_bulk_workload(
    workload_data: Sequence[Dict[str, Any]],
    ignore_failures: bool = False,
    skip_successes: bool = False,
    dry_run: bool = False,
) -> Tuple[Sequence[Mapping[str, Any]], int]:
    """
    Deploy a workloads in bulk based on the input file.

    :param workload_data: workload deployment information.
    :param ignore_failures: continue if any deployment fails.
    :param skip_successes: skip any deployment already marked with success.
    :param skip_successes: validate inputs only.

    :return: a boolean indicating whether the bulk-workload deployment operation was successful.

    """

    data: List[WorkloadTemplateData] = []

    errors = 0
    workloads: Dict[str, int] = Counter()

    client = login_client_on_current_url()

    acps: Dict[str, ACP] = {}
    apps: Dict[str, App] = {}

    for i, entry in enumerate(workload_data):
        entry["status"] = None
        try:
            info = WorkloadTemplateData.parse_obj(entry)
        except Exception as e:
            logger.error(f"Invalid entry: {i + 1}:\n{indent(str(e), ' ' * 2)}")
            entry["status"] = "invalid data"
            errors += 1
            continue

        data += [info]
        workloads[info.workload_name] += 1

        if info.acp_name not in acps:
            try:
                acps[info.acp_name] = client.acp.get_acp(acp_name=info.acp_name)
            except APIError:
                logger.error(f"Unknown ACP: {i + 1}: {info.acp_name}")
                entry["status"] = "unknown acp name"
                errors += 1
                continue

        try:
            app = apps.get(info.app_name) or client.app.get_app(app_name=info.app_name)
        except APIError:
            logger.error(f"Unknown app name: {i + 1}: {info.app_name}")
            entry["status"] = "unknown app name"
            errors += 1
            continue

        if not any(x.version == info.app_version for x in app.versions or []):
            logger.error(f"Unknown app version: {i + 1}: {info.app_version}")
            entry["status"] = "unknown app version"
            errors += 1

    if errors:
        logger.error(f"Total errors: {errors}")
        return workload_data, errors

    duplicates = {k: v for k, v in workloads.items() if v > 1}
    if duplicates:
        for info in data:
            if info.workload_name in duplicates:
                info.status = "duplicate workload"
        duplicate_names = "\n".join(f"  - {k}: {v}" for k, v in sorted(duplicates.items()))
        logger.error(f"Duplicated workload definitions:\n{duplicate_names}")
        return [x.dict() for x in data], len(duplicates)

    app_configs: List[KelvinAppConfiguration] = []

    errors = 0
    logger.info("Generating runtime configuration.")
    for i, info in tqdm(enumerate(data), "generating runtime configuration", total=len(data)):
        try:
            info_app_config: KPath = info.app_config
            obj = info_app_config.read_yaml(context=info.dict(), delimiter_style=DelimiterStyle.ANGULAR)
            app_configs += [KelvinAppConfiguration.parse_obj(obj)]
        except Exception as e:
            logger.error(f"Invalid runtime configuration: {i}:\n{indent(str(e), ' ' * 2)}")
            info.status = "invalid runtime"
            errors += 1
        else:
            info.status = "valid"

    if errors:
        logger.error(f"Total errors: {errors}")
        return [x.dict() for x in data], errors

    if dry_run:
        logger.info("Dry run only - no errors")
        return [x.dict() for x in data], errors

    logger.info("Deploying workloads")
    progress = tqdm(total=len(data), desc=" " * 32)

    errors = 0

    for i, (info, app_config) in enumerate(zip(data, app_configs)):
        if info.result == "skip" or (skip_successes and info.result == "success"):
            progress.update()
            continue

        progress.set_description(info.workload_name.ljust(32))

        with NamedTemporaryFile("wt") as temp_file:
            temp_file.write(app_config.json(exclude_none=True))
            temp_file.flush()

            workload_deployment_request = WorkloadDeploymentRequest(
                acp_name=info.acp_name,
                app_name=info.app_name,
                app_version=info.app_version,
                workload_name=info.workload_name,
                workload_title=info.workload_title,
                app_config=temp_file.name,
                quiet=True,
            )
            result = workload_deploy(workload_deployment_request=workload_deployment_request)

        if result:
            info.result = "success"
        else:
            errors += 1
            info.result = "failed"
            if ignore_failures or display_yes_or_no_question("Workload deployment failed. Continue?"):
                logger.warning(f"Skipping failed workload deployment: {i + 1}: {info.workload_name}")
            else:
                logger.warning(f"Stopping after failed workload deployment: {i + 1}: {info.workload_name}")
                break

        progress.update()

    if errors:
        logger.error(f"Total errors: {errors}")

    return [x.dict() for x in data], errors
