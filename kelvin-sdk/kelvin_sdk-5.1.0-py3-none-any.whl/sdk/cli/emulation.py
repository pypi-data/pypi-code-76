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
from typing import Optional, Sequence, Tuple

import click

from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs, KSDKHelpMessages
from kelvin.sdk.lib.common.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def emulation() -> bool:
    """
    Emulate and test applications locally.
    """


@emulation.command(cls=KSDKCommand)
@click.argument("app_name", nargs=1, type=click.STRING, required=False)
@click.option("--app-config", type=click.Path(exists=True), required=False, help=KSDKHelpMessages.emulation_app_config)
@click.option("--net-alias", type=click.STRING, required=False, help=KSDKHelpMessages.net_alias)
@click.option("--port-mapping", type=click.STRING, multiple=True, required=False, help=KSDKHelpMessages.port_mapping)
@click.option("--shared-dir", type=click.STRING, help=KSDKHelpMessages.shared_dir, show_default=True)
@click.option("--show-logs", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.show_logs)
def start(
    app_name: str,
    app_config: str,
    net_alias: str,
    shared_dir: str,
    port_mapping: Tuple[str],
    show_logs: bool,
) -> bool:
    """
    Start an application in the emulation system.

    """
    from kelvin.sdk.interface import emulation_start

    return emulation_start(
        app_name=app_name,
        app_config=app_config,
        net_alias=net_alias,
        shared_dir=shared_dir,
        port_mapping=list(port_mapping),  # is a tuple by default
        show_logs=show_logs,
    )


@emulation.command(cls=KSDKCommand)
@click.argument("app_name", type=click.STRING, nargs=1, required=False)
def stop(app_name: str) -> bool:
    """
    Stop an application running in the application system.

    """
    from kelvin.sdk.interface import emulation_stop

    return emulation_stop(app_name=app_name)


@emulation.command(cls=KSDKCommand)
@click.argument("app_name", type=click.STRING, nargs=1, required=False)
@click.option("--tail", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.emulation_logs_tail_lines)
def logs(app_name: str, tail: bool) -> bool:
    """
    Show the logs of an application running in the emulation system.

    """
    from kelvin.sdk.interface import emulation_logs

    return emulation_logs(app_name=app_name, tail=tail)


@emulation.command(cls=KSDKCommand)
@click.argument("app_name", type=click.STRING, nargs=1, required=False)
@click.option("--entrypoint", type=click.STRING, required=True, help=KSDKHelpMessages.entry_point)
@click.option("--interactive", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.test_interactive)
@click.argument("args", type=click.STRING, nargs=-1, required=False)
def test(app_name: Optional[str], entrypoint: str, interactive: bool, args: Sequence[str]) -> bool:
    """
    Run a test script for an application.

    """
    from kelvin.sdk.interface import emulation_test

    return emulation_test(app_name=app_name, entrypoint=entrypoint, interactive=interactive, args=args)


@emulation.command(cls=KSDKCommand)
@click.argument("input_file", type=click.Path(exists=True), nargs=-1, required=True)
@click.option("--app-name", multiple=True, required=True, help=KSDKHelpMessages.data_injector_app_name)
@click.option("--endpoint", default=None, show_default=True, help=KSDKHelpMessages.data_injector_endpoint)
@click.option(
    "--period",
    type=click.FLOAT,
    default=1.0,
    show_default=True,
    help=KSDKHelpMessages.data_injector_poller_period,
)
@click.option("--repeat", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.data_injector_repeat)
@click.option(
    "--ignore-timestamps",
    is_flag=True,
    default=False,
    show_default=True,
    help=KSDKHelpMessages.data_injector_ignore_timestamps,
)
def inject(
    input_file: Sequence[str],
    app_name: Sequence[str],
    endpoint: Optional[str],
    period: float,
    repeat: bool,
    ignore_timestamps: bool,
) -> bool:
    """
    Initializes the default injector application.
    This application will take the input file provided and inject it into the bus.

    Supported file types: ".csv", ".parquet".

    A compressed zip file with the valid types is supported.

    """

    from kelvin.sdk.interface import data_inject

    return data_inject(
        input_file=input_file,
        app_name=app_name,
        endpoint=endpoint,
        period=period,
        repeat=repeat,
        ignore_timestamps=ignore_timestamps,
    )


@emulation.command(cls=KSDKCommand)
@click.argument("app_name", nargs=-1, required=True)
@click.option(
    "--shared-dir",
    type=click.STRING,
    default=GeneralConfigs.default_shared_dir,
    help=KSDKHelpMessages.shared_dir,
    show_default=True,
)
@click.option("--batch", type=click.FLOAT, default=15.0, show_default=True, help=KSDKHelpMessages.data_extractor_batch)
def extract(app_name: Sequence[str], shared_dir: str, batch: float) -> bool:
    """
    Initializes the default extractor application.

    """
    from kelvin.sdk.interface import data_extract

    return data_extract(app_name=app_name, shared_dir=shared_dir, batch=batch)
