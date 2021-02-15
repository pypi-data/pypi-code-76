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
def datamodel_list(all_datamodels: bool = False, should_display: bool = False) -> List[DisplayObject]:
    """
    Returns the list of datamodels available on the system.

    :param all_datamodels: Indicates whether the list operation should yield all datamodels and its respective versions.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the Datamodels available on the platform.

    """
    from kelvin.sdk.lib.common.api.datamodel import datamodel_list as _datamodel_list

    return _datamodel_list(all_datamodels=all_datamodels, query=None, should_display=should_display)


@typechecked
def datamodel_search(query: Optional[str] = None, should_display: bool = False) -> List[DisplayObject]:
    """
    Search for datamodels on the platform that match the provided query.

    :param query: the query to search for.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the Datamodels available on the platform.

    """
    from kelvin.sdk.lib.common.api.datamodel import datamodel_list as _datamodel_list

    return _datamodel_list(all_datamodels=True, query=query, should_display=should_display)


@typechecked
def datamodel_show(
    datamodel_name: str, datamodel_version: Optional[str], should_display: bool = True
) -> List[DisplayObject]:
    """
    Displays the details on a specific datamodel.

    :param datamodel_name: the name of the datamodel to show.
    :param datamodel_version: the version of the datamodel to show. Latest if none is provided.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the yielded datamodel and its data.

    """
    from kelvin.sdk.lib.common.api.datamodel import datamodel_show as _datamodel_show

    return _datamodel_show(
        datamodel_name=datamodel_name, datamodel_version=datamodel_version, should_display=should_display
    )


@typechecked
def datamodel_create(datamodel_name: str, output_dir: Optional[str]) -> bool:
    """
    Creates a datamodel from the specified parameters.

    :param datamodel_name: the name of the datamodel to create.
    :param output_dir: the output directory where the datamodel will be created.

    :return: a boolean indicating whether the datamodel was successfully created.

    """
    from kelvin.sdk.lib.common.datamodels.datamodel_manager import create_datamodel as _create_datamodel

    return _create_datamodel(datamodel_name=datamodel_name, output_dir=output_dir)


@typechecked
def datamodel_upload(input_dir: Optional[str], datamodels: Optional[List[str]]) -> bool:
    """
    Upload all the datamodels in the provided input directory.

    :param input_dir: the directory to read the data models from.
    :param datamodels: the names of the datamodels to upload.

    :return: a boolean indicating the end of the datamodel upload operation.

    """
    from kelvin.sdk.lib.common.datamodels.datamodel_manager import upload_datamodels as _upload_datamodels

    return _upload_datamodels(input_dir=input_dir, datamodels=datamodels)


@typechecked
def datamodel_download(datamodel_name: str, datamodel_version: str, output_dir: Optional[str]) -> bool:
    """
    Download the datamodel corresponding to the provided datamodel id into the provided output dir.

    :param datamodel_name: the name of the datamodel to download.
    :param datamodel_version: the version of the datamodel to download.
    :param output_dir: the path into which the datamodel should be downloaded.

    :return: a boolean indicating the end of the datamodel download operation.

    """
    from kelvin.sdk.lib.common.datamodels.datamodel_manager import download_datamodel as _download_datamodel

    return _download_datamodel(
        datamodel_name=datamodel_name, datamodel_version=datamodel_version, output_dir=output_dir
    )


@typechecked
def datamodel_extract_schema(input_dir: str, output_dir: str, datamodels: Optional[List[str]]) -> bool:
    """
    Extract the schema of the provided data models.

    :param input_dir: the directory to read the data models from.
    :param output_dir: the directory to output the schemas of the datamodels.
    :param datamodels: the names of the data models to extract the schema from.

    :return: a boolean indicating the end of the datamodel extraction operation.

    """
    from kelvin.sdk.lib.common.datamodels.datamodel_manager import datamodel_extract_schema as _datamodel_extract_schema

    return _datamodel_extract_schema(input_dir=input_dir, output_dir=output_dir, datamodels=datamodels)
