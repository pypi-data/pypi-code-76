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

from kelvin.sdk.lib.common.emulation.emulation_manager import emulation_start
from kelvin.sdk.lib.common.models.factories.app_setup_configuration_objects_factory import get_default_app_name
from kelvin.sdk.lib.common.utils.logger_utils import logger


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
    try:
        if app_name is not None and ":" not in app_name:
            args = (app_name, *args)
            app_name = None

        app_name = app_name or get_default_app_name()

        logger.info("Running test script.")

        if not args:
            full_entrypoint = entrypoint
        else:
            full_entrypoint = f"{entrypoint} {' '.join(args)}"

        emulation_start_entrypoint = f"env PYTHONPATH=/opt/kelvin/app {full_entrypoint}"

        start_app_result = emulation_start(
            app_name=app_name,
            net_alias=None,
            app_config_path=None,
            port_mapping=None,
            shared_dir_path=None,
            entrypoint=emulation_start_entrypoint,
            attach=interactive,
        )

        logger.info(f'Test script for "{app_name}" successfully executed')

        return start_app_result

    except Exception as exc:
        logger.exception(f"Error executing test script: {str(exc)}")
        return False
