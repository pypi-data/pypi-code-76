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

from typing import List, Optional, Sequence

from typeguard import typechecked


@typechecked
def emulation_start(
    app_name: Optional[str],
    app_config: Optional[str],
    net_alias: Optional[str],
    shared_dir: Optional[str],
    port_mapping: Optional[List[str]],
    show_logs: bool = False,
) -> bool:
    """
    Start an application on the emulation system.

    :param app_name: the application's name.
    :param app_config: the app configuration file to be used on the emulation.
    :param net_alias: the network alias.
    :param port_mapping: the port to be mapped between the container and the host machine.
    :param shared_dir: the path to the desired shared dir.
    :param show_logs: if provided, will start displaying longs once the app is emulated.

    :return: a boolean indicating whether the App was successfully started.

    """
    from kelvin.sdk.lib.common.emulation.emulation_manager import emulation_start as _emulation_start

    return _emulation_start(
        app_name=app_name,
        app_config_path=app_config,
        net_alias=net_alias,
        port_mapping=port_mapping,
        shared_dir_path=shared_dir,
        show_logs=show_logs,
    )


@typechecked
def emulation_stop(app_name: Optional[str], should_stop_network: bool = True) -> bool:
    """
    Stop a running application.

    :param app_name: the name of the app to stop.
    :param should_stop_network: indicates whether the ksdk network should also be stopped.

    :return: a boolean indicating whether the App was successfully stopped.

    """
    from kelvin.sdk.lib.common.emulation.emulation_manager import emulation_stop as _emulation_stop

    return _emulation_stop(app_name=app_name, should_stop_network=should_stop_network)


@typechecked
def emulation_logs(app_name: Optional[str], tail: bool = False) -> bool:
    """
    Display the logs of a running application.

    :param app_name: the name of the application to retrieve the logs from.
    :param tail: indicates whether it should tail the logs and return.

    :return: a symbolic flag indicating the logs were successfully obtained.

    """
    from kelvin.sdk.lib.common.emulation.emulation_manager import emulation_logs as _emulation_logs

    return _emulation_logs(app_name=app_name, tail=tail)


@typechecked
def emulation_test(
    app_name: Optional[str], entrypoint: str, interactive: bool = False, args: Sequence[str] = ()
) -> bool:
    """
    Run a test to run on the emulation system.

    :param app_name: the name of the app to run the test command on.
    :param entrypoint: the test entrypoint to be executed on.
    :param interactive: run command interactively.
    :param args: the optional args for the entrypoint.

    :return: a bool indicating the emulation test was successfully executed.

    """
    from kelvin.sdk.lib.common.emulation.emulation_tests_manager import emulation_test as _emulation_test

    return _emulation_test(app_name=app_name, entrypoint=entrypoint, interactive=interactive, args=args)


@typechecked
def data_inject(
    input_file: Sequence[str],
    app_name: Sequence[str],
    endpoint: Optional[str],
    period: float,
    repeat: bool,
    ignore_timestamps: bool,
) -> bool:
    """
    Start the embedded Injector app that will inject data into the emulation system..

    :param input_file: the sequence of files that will be injected into the system.
    :param app_name: the app into which the data will be injected.
    :param endpoint: the endpoint to publish data into.
    :param period: the rate at which data will be polled from the application.
    :param repeat: indicates whether the injection should repeat forever.
    :param ignore_timestamps: ignore timestamps in data.

    :return: a boolean indicating whether the injector was successfully started.

    """

    from kelvin.sdk.lib.common.apps.local_apps_manager import start_data_injector as _start_data_injector

    return _start_data_injector(
        input_file=input_file,
        app_name=app_name,
        endpoint=endpoint,
        period=period,
        repeat=repeat,
        ignore_timestamps=ignore_timestamps,
    )


@typechecked
def data_extract(app_name: Sequence[str], shared_dir: str, batch: float) -> bool:
    """
    Start the embedded Extractor app that will extract data from the emulation system..

    :param app_name: the sequence of apps to extract data from.
    :param shared_dir: the directory shared between the container and the host machine.
    :param batch: the extractor batch write frequency.

    :return: a boolean indicating whether the extractor was successfully started.

    """

    from kelvin.sdk.lib.common.apps.local_apps_manager import start_data_extractor as _start_data_extractor

    return _start_data_extractor(app_name=app_name, shared_dir=shared_dir, batch=batch)
