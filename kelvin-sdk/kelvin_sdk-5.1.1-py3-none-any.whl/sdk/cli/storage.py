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

import re
from typing import Any, Optional, Union

import click
from click import Choice, Context, Option, Parameter

from kelvin.sdk.lib.common.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.common.models.types import Aggregates, Formats, TimeUnit
from kelvin.sdk.lib.common.utils.click_utils import KSDKCommand, KSDKGroup


def check_duration(ctx: Context, param: Union[Option, Parameter], value: Optional[str]) -> Optional[str]:
    """Check time units."""

    if value is None:
        return value

    value = value.strip()

    component_re = re.compile(r"([^0-9a-z]*)([0-9]+)([a-z]+)([^0-9a-z]*)")

    components = component_re.findall(value)
    if not components:
        ctx.fail(f"{param.name.replace('_', '-')}: {value!r} is not a valid duration")

    unit_order = {unit.value: i for i, unit in enumerate(reversed(TimeUnit))}

    i = -1
    for component in components:
        left, x, unit, right = component
        if left or right:
            if left:
                left = f"({left})"
            if right:
                right = f"({right})"
            ctx.fail(f"{param.name.replace('_', '-')}: extra characters in duration: {left}{x}{unit}{right}")
        order = unit_order.get(unit)
        if order is None:
            ctx.fail(f"{param.name.replace('_', '-')}: {''.join(component)!r} does not contain a valid unit")
        if i >= order:
            ctx.fail(f"{param.name.replace('_', '-')}: units are not in descending order")
        i = order

    return value


@click.group(cls=KSDKGroup)
def storage() -> bool:
    """
    Retrieve storage data from the platform.

    """


@storage.command(cls=KSDKCommand, name="list")
@click.option("--acp-name", type=click.STRING, help=KSDKHelpMessages.storage_acp_name)
@click.option("--source", type=click.STRING, help=KSDKHelpMessages.storage_source)
@click.option("--key", type=click.STRING, help=KSDKHelpMessages.storage_key)
@click.option("data_type", "--type", type=click.STRING, help=KSDKHelpMessages.storage_type)
def storage_list(acp_name: str, source: str, key: str, data_type: str) -> bool:
    """
    List the available storage entries on the platform.

    """
    from kelvin.sdk.interface import storage_list as _storage_list

    return bool(_storage_list(acp_name=acp_name, source=source, key=key, data_type=data_type, should_display=True))


@click.group(cls=KSDKGroup)
def get() -> bool:
    """
    Retrieve storage data from specific parameters.

    """


@get.command(cls=KSDKCommand, name="range")
@click.option("--acp-name", type=click.STRING, required=True, help=KSDKHelpMessages.storage_acp_name)
@click.option("--source", type=click.STRING, required=True, help=KSDKHelpMessages.storage_source)
@click.option("--key", type=click.STRING, required=True, help=KSDKHelpMessages.storage_key)
@click.option("--start-date", type=click.STRING, required=True, help=KSDKHelpMessages.storage_start_date)
@click.option("--end-date", type=click.STRING, required=True, help=KSDKHelpMessages.storage_end_date)
@click.option("data_type", "--type", type=click.STRING, required=True, help=KSDKHelpMessages.storage_type)
@click.option("--agg", type=Choice(Aggregates.as_list()), help=KSDKHelpMessages.storage_agg)
@click.option("--time-bucket", callback=check_duration, help=KSDKHelpMessages.storage_time_bucket)
@click.option("--time-shift", callback=check_duration, help=KSDKHelpMessages.storage_time_shift)
@click.option("--output-file", type=click.STRING, help=KSDKHelpMessages.storage_output_file)
@click.option("--output-format", type=Choice(Formats.as_list()), help=KSDKHelpMessages.storage_output_format)
@click.option("--pivot", is_flag=True, default=False, show_default=True, help=KSDKHelpMessages.storage_pivot)
def storage_range(
    acp_name: str,
    source: str,
    key: str,
    start_date: str,
    end_date: str,
    data_type: str,
    agg: Optional[str],
    time_bucket: Optional[str],
    time_shift: Optional[str],
    output_file: Optional[str],
    output_format: str,
    pivot: bool,
) -> bool:
    """
    Retrieve a range of storage data.

    """
    from kelvin.sdk.interface import storage_get_range

    return (
        storage_get_range(
            acp_name=acp_name,
            source=source,
            key=key,
            data_type=data_type,
            start_date=start_date,
            end_date=end_date,
            agg=agg,
            time_bucket=time_bucket,
            time_shift=time_shift,
            output_file=output_file,
            output_format=output_format,
            pivot=pivot,
            should_display=True,
        )
        is not None
    )


@get.command(cls=KSDKCommand)
@click.option("--acp-name", type=click.STRING, required=True, help=KSDKHelpMessages.storage_acp_name)
@click.option("--source", type=click.STRING, required=True, help=KSDKHelpMessages.storage_source)
@click.option("--key", type=click.STRING, required=True, help=KSDKHelpMessages.storage_key)
@click.option("data_type", "--type", type=click.STRING, required=True, help=KSDKHelpMessages.storage_type)
def last(acp_name: str, source: str, key: str, data_type: str) -> Optional[Any]:
    """
    Retrieve the last storage information for the specified parameters.

    """
    from kelvin.sdk.interface import storage_get_last

    return storage_get_last(acp_name=acp_name, source=source, key=key, data_type=data_type, should_display=True)


storage.add_command(get)
