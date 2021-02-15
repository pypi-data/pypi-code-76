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
from typing import List, Tuple

import click

from kelvin.sdk.lib.common.configs.internal.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.common.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def datamodel() -> bool:
    """
    Manage and view data models.

    """


@datamodel.command(cls=KSDKCommand, name="list")
@click.option("all_datamodels", "--all", is_flag=True, show_default=True, help=KSDKHelpMessages.datamodel_list_all)
def list_datamodels(all_datamodels: bool) -> List:
    """
    List the data models available on the platform.

    """
    from kelvin.sdk.interface import datamodel_list

    return datamodel_list(all_datamodels=all_datamodels, should_display=True)


@datamodel.command(cls=KSDKCommand)
@click.argument("query", type=click.STRING, nargs=1)
def search(query: str) -> List:
    """
    Search for specific data models available on the platform.

    e.g. kelvin datamodel search "my.model"
    """
    from kelvin.sdk.interface import datamodel_search

    return datamodel_search(query=query, should_display=True)


@datamodel.command(cls=KSDKCommand)
@click.argument("data_model", type=click.STRING, nargs=1)
@click.option(
    "--output-dir",
    type=click.STRING,
    help=KSDKHelpMessages.datamodel_create_output_dir,
)
def create(data_model: str, output_dir: str) -> bool:
    """
    Create a basic data model spec file from the provided name.

    e.g. kelvin datamodel create "my.model"
    """
    from kelvin.sdk.interface import datamodel_create

    return datamodel_create(datamodel_name=data_model, output_dir=output_dir)


@datamodel.command(cls=KSDKCommand)
@click.argument("data_model", type=click.STRING, nargs=1)
@click.option("--version", type=click.STRING, required=False, help=KSDKHelpMessages.datamodel_show_version)
def show(data_model: str, version: str) -> List:
    """
    Displays the details on a specific datamodel.

    e.g. kelvin datamodel show "my.model" --version=1.0.0
    """
    from kelvin.sdk.interface import datamodel_show

    return datamodel_show(datamodel_name=data_model, datamodel_version=version, should_display=True)


@datamodel.command(cls=KSDKCommand)
@click.option(
    "--input-dir",
    type=click.STRING,
    help=KSDKHelpMessages.datamodel_upload_input_dir,
)
@click.option(
    "datamodels",
    "--names",
    type=click.STRING,
    multiple=True,
    required=False,
    help=KSDKHelpMessages.datamodel_upload_names,
)
def upload(input_dir: str, datamodels: Tuple[str]) -> bool:
    """
    Upload data models to the platform.

    e.g. kelvin datamodel upload --names=my.model:1.0.0
    """
    from kelvin.sdk.interface import datamodel_upload

    # transform into list and remove duplicates
    clean_datamodels = list(set(datamodels))
    return datamodel_upload(input_dir=input_dir, datamodels=clean_datamodels)


@datamodel.command(cls=KSDKCommand)
@click.argument("name", type=click.STRING, nargs=1)
@click.argument("version", type=click.STRING, nargs=1)
@click.option(
    "--output-dir",
    type=click.STRING,
    help=KSDKHelpMessages.datamodel_download_output_dir,
)
def download(name: str, version: str, output_dir: str) -> bool:
    """
    Download a data model from the platform.

    e.g. kelvin datamodel download "my.model" "1.0.0" --output-dir=my_dir/
    """
    from kelvin.sdk.interface import datamodel_download

    return datamodel_download(datamodel_name=name, datamodel_version=version, output_dir=output_dir)


@datamodel.command(cls=KSDKCommand)
@click.option("--input-dir", type=click.STRING, help=KSDKHelpMessages.datamodel_extract_schema_input_dir, required=True)
@click.option(
    "--output-dir", type=click.STRING, help=KSDKHelpMessages.datamodel_extract_schema_output_dir, required=True
)
@click.option(
    "datamodels",
    "--names",
    type=click.STRING,
    multiple=True,
    required=False,
    help=KSDKHelpMessages.datamodel_extract_schema_names,
)
def extract_schema(input_dir: str, output_dir: str, datamodels: Tuple[str]) -> bool:
    """
    Extract the schema of the provided data models.

    e.g. kelvin datamodel extract-schema --input-dir=datamodel/ --output-dir=schemas/
    """
    from kelvin.sdk.interface import datamodel_extract_schema

    # transform into list and remove duplicates
    clean_datamodels = list(set(datamodels))
    return datamodel_extract_schema(input_dir=input_dir, output_dir=output_dir, datamodels=clean_datamodels)
