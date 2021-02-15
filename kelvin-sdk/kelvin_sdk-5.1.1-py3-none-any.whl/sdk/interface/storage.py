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

from kelvin.sdk.lib.common.utils.display_utils import DisplayObject


@typechecked
def storage_list(
    acp_name: Optional[str],
    source: Optional[str],
    key: Optional[str],
    data_type: Optional[str],
    should_display: bool = False,
) -> List[DisplayObject]:
    """
    Returns the list of storage metrics from the platform.

    :param acp_name: The name of the ACP to filter the search.
    :param source: The source of data.
    :param key: The key to query for.
    :param data_type: The data type to query for.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the storage metrics available on the platform.

    """
    from kelvin.sdk.lib.common.api.storage import storage_list as _storage_list

    return _storage_list(acp_name=acp_name, source=source, key=key, data_type=data_type, should_display=should_display)


@typechecked
def storage_get_range(
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
    output_format: Optional[str],
    pivot: bool,
    should_display: bool = False,
) -> List[DisplayObject]:
    """
    Displays all the details of the specified acp from the platform.

    :param acp_name: The name of the ACP to filter the search.
    :param source: The source of data.
    :param key: The key to query for.
    :param start_date: The start date to filter the retrieval of storage data.
    :param end_date: The end date to filter the retrieval of storage data.
    :param data_type: The data type to query for.
    :param agg: The aggregate value to aggregate the data for.
    :param time_bucket: The bucket of time to apply on the aggregation.
    :param time_shift: The time period offset step for the time-bucket.
    :param output_file: The file to output the data into.
    :param output_format: The file format for the output data.
    :param selectors: Optional selectors.
    :param pivot: Pivot result into columns.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the storage data matching the provided range.

    """
    from kelvin.sdk.lib.common.api.storage import storage_get_range as _storage_get_range

    return _storage_get_range(
        agg=agg,
        acp_name=acp_name,
        source=source,
        key=key,
        start_date=start_date,
        end_date=end_date,
        data_type=data_type,
        time_bucket=time_bucket,
        time_shift=time_shift,
        output_file=output_file,
        output_format=output_format,
        pivot=pivot,
        should_display=should_display,
    )


@typechecked
def storage_get_last(
    acp_name: str, source: str, key: str, data_type: str, should_display: bool = False
) -> List[DisplayObject]:
    """
    Returns the last storage info for the provided parameters from the platform.

    :param acp_name: The name of the ACP to filter the search.
    :param source: The source of data.
    :param key: The key to query for.
    :param data_type: The data type to query for.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the storage metrics available on the platform.

    """
    from kelvin.sdk.lib.common.api.storage import storage_get_last as _storage_get_last

    return _storage_get_last(
        acp_name=acp_name, source=source, key=key, data_type=data_type, should_display=should_display
    )
