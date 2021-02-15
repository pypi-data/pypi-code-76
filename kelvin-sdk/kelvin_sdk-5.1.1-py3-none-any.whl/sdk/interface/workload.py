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

from typing import List, Optional

from typeguard import typechecked

from kelvin.sdk.interface import StatusDataSource
from kelvin.sdk.lib.common.models.ksdk_workload_deployment import WorkloadDeploymentRequest
from kelvin.sdk.lib.common.utils.display_utils import DisplayObject


@typechecked
def workload_list(
    acp_name: Optional[str],
    app_name: Optional[str],
    app_version: Optional[str],
    enabled: bool,
    source: StatusDataSource,
    should_display: bool = False,
) -> List[DisplayObject]:
    """
    Returns the list of workloads filtered any of the arguments.

    :param acp_name: the name of the acp to filter the workloads.
    :param app_name: the name of the app to filter the workloads.
    :param app_version: the version of the acp to filter the workloads.
    :param enabled: indicates whether it should filter workloads by their status.
    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the workloads available on the platform.

    """
    from kelvin.sdk.lib.common.api.workload import workload_list as _workload_list

    return _workload_list(
        acp_name=acp_name,
        app_name=app_name,
        app_version=app_version,
        enabled=enabled,
        source=source,
        should_display=should_display,
    )


@typechecked
def workload_search(query: str, source: StatusDataSource, should_display: bool = False) -> List[DisplayObject]:
    """
    Search for workloads matching the provided query.

    :param query: the query to search for.
    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the matching workloads on the platform.

    """
    from kelvin.sdk.lib.common.api.workload import workload_list as _workload_list

    return _workload_list(query=query, source=source, should_display=should_display)


@typechecked
def workload_show(workload_name: str, source: StatusDataSource, should_display: bool = False) -> List[DisplayObject]:
    """
    Show the details of the specified workload.

    :param workload_name: the name of the workload.
    :param source: the status data source from where to obtain data.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the yielded workload and its data.

    """
    from kelvin.sdk.lib.common.api.workload import workload_show as _workload_show

    return _workload_show(workload_name=workload_name, source=source, should_display=should_display)


@typechecked
def workload_deploy(workload_deployment_request: WorkloadDeploymentRequest) -> bool:
    """
    Deploy a workload from the specified deploy request.

    :param workload_deployment_request: the deployment object that encapsulates all the necessary parameters for deploy.

    :return: a boolean indicating whether the workload deploy operation was successful.

    """
    from kelvin.sdk.lib.common.api.workload import workload_deploy as _workload_deploy

    return _workload_deploy(workload_deployment_request=workload_deployment_request)


@typechecked
def workload_update(
    workload_name: str, app_version: Optional[str], workload_title: Optional[str], app_config: str
) -> bool:
    """
    Update an existing workload with the new parameters.

    :param workload_name: the name for the workload to update.
    :param app_version: the the version of the app.
    :param workload_title: the title for the  workload.
    :param app_config: the path to the app configuration file.

    :return: a boolean indicating whether the workload update operation was successful.

    """
    from kelvin.sdk.lib.common.api.workload import workload_update as _workload_update

    return _workload_update(
        workload_name=workload_name,
        workload_title=workload_title,
        app_version=app_version,
        app_config=app_config,
    )


@typechecked
def workload_logs(workload_name: str, tail_lines: int, output_file: Optional[str], follow: bool) -> bool:
    """
    Show the logs of a deployed workload.

    :param workload_name: the name of the workload.
    :param tail_lines: the number of lines to retrieve on the logs request.
    :param output_file: the file to output the logs into.
    :param follow: a flag that indicates whether it should trail the logs, constantly requesting for more logs.

    :return: a boolean indicating the end of the workload show logs operation.

    """
    from kelvin.sdk.lib.common.api.workload import workload_logs as _workload_logs

    return _workload_logs(
        workload_name=workload_name, tail_lines=str(tail_lines), output_file=output_file, follow=follow
    )


@typechecked
def workload_undeploy(workload_name: str, ignore_destructive_warning: bool) -> bool:
    """
    Stop and delete a workload on the platform.

    :param workload_name: the name of the workload to be stopped and deleted.
    :param ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    :return: a boolean indicating the end of the workload deletion operation.

    """
    from kelvin.sdk.lib.common.api.workload import workload_undeploy as _workload_undeploy

    return _workload_undeploy(workload_name=workload_name, ignore_destructive_warning=ignore_destructive_warning)


@typechecked
def workload_start(workload_name: str) -> bool:
    """
    Start the provided workload.

    :param workload_name: the workload to start on the platform.

    :return: a boolean indicating the end of the workload start operation.

    """
    from kelvin.sdk.lib.common.api.workload import workload_start as _workload_start

    return _workload_start(workload_name=workload_name)


@typechecked
def workload_stop(workload_name: str, ignore_destructive_warning: bool) -> bool:
    """
    Stop the provided workload.

    :param workload_name: the workload to stop on the platform.
    :param ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    :return: a boolean indicating the end of the workload stop operation.

    """
    from kelvin.sdk.lib.common.api.workload import workload_stop as _workload_stop

    return _workload_stop(workload_name=workload_name, ignore_destructive_warning=ignore_destructive_warning)


@typechecked
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

    from kelvin.sdk.lib.common.api.workload import workload_deploy_bulk

    return workload_deploy_bulk(
        filename=filename,
        file_type=file_type,
        output_filename=output_filename,
        ignore_failures=ignore_failures,
        skip_successes=skip_successes,
        dry_run=dry_run,
    )
