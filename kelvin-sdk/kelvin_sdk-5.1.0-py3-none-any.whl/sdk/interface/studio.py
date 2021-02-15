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
from typing import Optional

from typeguard import typechecked

from kelvin.sdk.lib.common.configs.internal.emulation_configs import StudioConfigs


@typechecked
def studio_start(schema_file: Optional[str], input_file: Optional[str], port: int = StudioConfigs.default_port) -> bool:
    """
    Starts Kelvin Studio to modify the provided input.

    :param schema_file: the schema file used to power the Kelvin Studio's interface.
    :param input_file: the input file to modify based on the schema file..
    :param port: the studio server port..

    :return: a bool indicating whether the kelvin studio was successfully started.

    """
    from kelvin.sdk.lib.common.apps.studio_manager import studio_start as _studio_start

    return _studio_start(schema_file=schema_file, input_file=input_file, port=port)


@typechecked
def studio_stop() -> bool:
    """
    Stops a Kelvin Studio.

    :return: a bool indicating whether the Kelvin Studio was successfully stopped.

    """
    from kelvin.sdk.lib.common.apps.studio_manager import studio_stop as _studio_stop

    return _studio_stop()
