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

import json
import re
from datetime import datetime
from time import time_ns
from typing import Iterable, List, Optional, cast

import pandas
import pyarrow
from pandas import DataFrame
from pyarrow import Table, schema
from pyarrow.parquet import write_to_dataset

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.io import storage_to_dataframe
from kelvin.sdk.client.model.responses import StorageData
from kelvin.sdk.lib.common.auth.auth_manager import (
    login_client_on_current_url,
    retrieve_error_message_from_api_exception,
)
from kelvin.sdk.lib.common.configs.internal.general_configs import NANO_SECONDS_OFFSET, GeneralConfigs
from kelvin.sdk.lib.common.models.generic import GenericObject, KPath
from kelvin.sdk.lib.common.utils.display_utils import DisplayObject, display_data_entries, display_data_object
from kelvin.sdk.lib.common.utils.logger_utils import logger

number_re = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$")


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
    try:
        logger.info("Retrieving storage information..")

        client = login_client_on_current_url()

        metrics_storage = client.storage.list_historian_metric(
            acp_name=acp_name, source=source, key=key, type=data_type
        )
        storage_info = cast(List, metrics_storage)

        display_obj = display_data_entries(
            data=storage_info,
            header_names=["ACP Name", "Source", "Key", "Type", "Updated"],
            attributes=["acp_name", "source", "key", "type", "updated"],
            table_title=GeneralConfigs.table_title.format(title="Storage Info"),
            should_display=should_display,
            no_data_message="No storage data available",
        )

        return [display_obj]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error retrieving storage information: {error_message}")

    except Exception as exc:
        logger.exception(f"Error retrieving storage information: {str(exc)}")

    return []


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
    :param data_type: The data type to query for.
    :param start_date: The start date to filter the retrieval of storage data.
    :param end_date: The end date to filter the retrieval of storage data.
    :param agg: The aggregate value to aggregate the data for.
    :param time_bucket: The bucket of time to apply on the aggregation.
    :param time_shift: The time period offset step for the time-bucket.
    :param output_file: The file to output the data into.
    :param output_format: The file format for the output data.
    :param pivot: Pivot result into columns.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the storage data matching the provided range.

    """
    try:
        logger.info("Retrieving storage data for range..")

        client = login_client_on_current_url()

        storage_data = client.storage.get_historian_metric_range(
            acp_name=acp_name,
            source=source,
            key=key,
            type=data_type,
            start_time=_convert_time(start_date),
            end_time=_convert_time(end_date),
            agg=agg,
            time_bucket=time_bucket,
            time_shift=time_shift,
        )

        if output_file is not None:
            output_path: Optional[KPath]
            if output_format is None or output_format == "json":
                output_path = _output_storage_data_to_json(storage_data=storage_data, output_file=output_file)
                logger.relevant(f'Successfully retrieved data to "{output_path.absolute()}"')
                return []

            if output_format == "parquet":
                output_path = _output_storage_data_to_parquet(storage_data=storage_data, output_file=output_file)
                logger.relevant(f'Successfully retrieved data to "{output_path.absolute()}"')
                return []

            output_path = _output_storage_data_to_pandas_io(
                storage_data=storage_data,
                output_file=output_file,
                output_format=output_format,
                pivot=pivot,
            )
            if output_path is not None:
                logger.relevant(f'Successfully retrieved data to "{output_path.absolute()}"')
            else:
                logger.relevant("No values retrieved")

        else:
            data_to_display = []
            try:
                for _ in range(0, 100):
                    storage = next(storage_data)
                    # variables
                    payload = str(storage["payload"])
                    obj_payload = f"{payload[:47]}..." if len(payload) > 50 else payload
                    storage_timestamp = storage["timestamp"]
                    if storage_timestamp:
                        storage_timestamp = datetime.fromtimestamp(storage_timestamp / NANO_SECONDS_OFFSET)
                    data_to_display.append(
                        GenericObject(
                            data={
                                "acp_name": storage["acp_name"],
                                "source": storage["source"],
                                "key": storage["key"],
                                "payload": obj_payload,
                                "timestamp": storage_timestamp,
                            }
                        )
                    )
            except StopIteration:
                pass

            display_obj = display_data_entries(
                data=data_to_display,
                header_names=["ACP Name", "Source", "Key", "Payload", "Timestamp"],
                attributes=["acp_name", "source", "key", "payload", "timestamp"],
                table_title=GeneralConfigs.table_title.format(title="Storage Info"),
                should_display=should_display,
                no_data_message="No storage data available",
            )

            if data_to_display:
                logger.relevant("Successfully retrieved data. Displaying the latest 100 entries")

            return [display_obj]

        return []

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error retrieving storage information for range: {error_message}")

    except TypeError:
        logger.exception(f"Error retrieving storage information for range: Could not retrieve any data yet")
    except Exception as exc:
        logger.exception(f"Error retrieving storage information for range: {str(exc)}")

    return []


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
    try:
        logger.info("Retrieving last storage data.")

        client = login_client_on_current_url()

        storage_data = client.storage.get_historian_metric_last(
            acp_name=acp_name, source=source, key=key, type=data_type
        )

        display_obj = display_data_object(data=storage_data, object_title="Storage Info", should_display=should_display)

        return [display_obj]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error retrieving storage information: {error_message}")

    except Exception as exc:
        logger.exception(f"Error retrieving storage information: {str(exc)}")

    return []


def _output_storage_data_to_json(storage_data: Iterable[StorageData], output_file: str) -> KPath:
    """
    Wrap up the creation of the storage data file.

    :param storage_data: the StorageData to output to a file.
    :param output_file: the output file to write the StorageData into.

    :return: the KPath the storage data was written into.

    """
    output_file_path = KPath(output_file)
    with open(output_file_path, "w") as file:
        for entry in storage_data:
            json.dump(entry.dict(), file, ensure_ascii=True, indent=4, sort_keys=True)
            file.write("\n")
    return output_file_path


def _output_storage_data_to_parquet(storage_data: Iterable[StorageData], output_file: str) -> KPath:
    """
    Wrap up the creation of the storage data file.

    :param storage_data: the StorageData to output to a file.
    :param output_file: the output file to write the StorageData into.

    :return: the KPath the storage data was written into.

    """
    output_file_path = KPath(output_file)

    data_schema = schema(
        {
            "acp_name": pyarrow.string(),
            "source": pyarrow.string(),
            "key": pyarrow.string(),
            "timestamp": pyarrow.timestamp("ns"),
            "field": pyarrow.string(),
            "value": pyarrow.string(),
        }
    )

    for chunk in storage_to_dataframe(storage_data, expand_payload="row", chunk_size=10_000):
        chunk = chunk.assign(value=chunk.value.apply(json.dumps))
        table = Table.from_pandas(chunk.reset_index(), data_schema)

        write_to_dataset(
            table,
            str(output_file_path),
            ["acp_name", "source"],
            coerce_timestamps="us",
            allow_truncated_timestamps=True,
        )

    return output_file_path


def _output_storage_data_to_pandas_io(
    storage_data: Iterable[StorageData], output_file: str, output_format: str, pivot: bool
) -> Optional[KPath]:
    """
    Wrap up the creation of the storage data file.

    :param storage_data: the StorageData to output to a file.
    :param output_file: the output file to write the StorageData into.
    :param pivot: Pivot result into columns.

    :return: the KPath the storage data was written into.

    """
    output_file_path = KPath(output_file)

    try:
        writer = getattr(pandas.DataFrame, f"to_{output_format}")
    except AttributeError:
        raise ValueError(f"Unknown output format {output_format!r}")

    df: DataFrame = storage_to_dataframe(storage_data, expand_payload="column" if pivot else "row")
    if df is None:
        return None

    df.reset_index(inplace=True)
    if output_format == "excel":
        df["timestamp"] = df.timestamp.dt.tz_convert("UTC").dt.tz_localize(None)

    writer(df, output_file, index=False)

    return output_file_path


def _convert_time(x: Optional[str]) -> int:
    """Convert timestamp."""

    if x is None:
        return time_ns()

    return int((float(x) if number_re.match(x) else datetime.fromisoformat(x).timestamp()) * 1e9)
