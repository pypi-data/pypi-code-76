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

from typing import Dict, List, Optional, cast

from kelvin.sdk.client import Client
from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import DataModelCreate, ICDPayload
from kelvin.sdk.client.model.responses import DataModel
from kelvin.sdk.lib.common.auth.auth_manager import (
    login_client_on_current_url,
    retrieve_error_message_from_api_exception,
)
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.models.datamodels import ICDPayloadHelper
from kelvin.sdk.lib.common.models.generic import KPath
from kelvin.sdk.lib.common.utils.display_utils import DisplayObject, display_data_entries, display_data_object
from kelvin.sdk.lib.common.utils.logger_utils import logger


def datamodel_list(
    query: Optional[str] = None, all_datamodels: bool = False, should_display: bool = False
) -> List[DisplayObject]:
    """
    Returns the list of datamodels available on the system.

    :param query: the query to search for.
    :param all_datamodels: Indicates whether the list operation should yield all datamodels and its respective versions.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the Datamodels available on the platform.

    """
    try:
        datamodel_list_step_1 = "Retrieving datamodels.."
        if query:
            datamodel_list_step_1 = f'Searching datamodels that match "{query}"'

        logger.info(datamodel_list_step_1)

        client = login_client_on_current_url()

        datamodels = cast(List, client.data_model.list_data_model(search=query, all=all_datamodels)) or []

        display_obj = display_data_entries(
            data=datamodels,
            header_names=["Model", "Type", "Version", "Created", "Updated"],
            attributes=["name", "type", "version", "updated", "created"],
            table_title=GeneralConfigs.table_title.format(title="Datamodels"),
            should_display=should_display,
            no_data_message="No datamodels available",
        )

        return [display_obj]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error listing datamodels: {error_message}")

    except Exception as exc:
        logger.exception(f"Error listing datamodels: {str(exc)}")

    return []


def datamodel_show(
    datamodel_name: str, datamodel_version: Optional[str], should_display: bool = False
) -> List[DisplayObject]:
    """
    Displays the details on a specific datamodel.

    :param datamodel_name: the name of the datamodel to show.
    :param datamodel_version: the version of the datamodel to show. Latest if none is provided.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the yielded datamodel and its data.

    """
    try:
        client = login_client_on_current_url()

        if not datamodel_version:
            logger.info(f'Retrieving datamodel "{datamodel_name}"')
            datamodel = client.data_model.get_data_model_latest_version(data_model_name=datamodel_name)
        else:
            logger.info(f'Retrieving datamodel "{datamodel_name}:{datamodel_version}"')
            datamodel = client.data_model.get_data_model(
                data_model_name=datamodel_name, data_model_version=datamodel_version
            )

        title = GeneralConfigs.table_title.format(title="Datamodel info")
        datamodel_data_display_object = display_data_object(
            data=datamodel, should_display=should_display, object_title=title
        )

        return [datamodel_data_display_object]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error showing datamodel: {error_message}")

    except Exception as exc:
        logger.exception(f"Error showing datamodel: {str(exc)}")

    return []


def datamodel_upload(datamodel_content: Dict, source: str) -> bool:
    """
    Upload a single datamodel to the platform, along with its corresponding source.

    :param datamodel_content: the datamodel to upload to the platform.
    :param source: the source corresponding to the datamodel.

    :return: a boolean indicating the datamodel was successfully uploaded.

    """
    try:
        client = login_client_on_current_url()

        icd_payload_helper = ICDPayloadHelper(**datamodel_content)

        datamodel_name_with_version = f"{icd_payload_helper.name}:{icd_payload_helper.version}"
        logger.info(f'Uploading datamodel "{datamodel_name_with_version}"')

        icd_payload = ICDPayload(**icd_payload_helper.dict())
        datamodel_create_payload = DataModelCreate(icd=icd_payload, source=source)
        client.data_model.create_data_model(data=datamodel_create_payload)

        logger.relevant(f'Datamodel "{icd_payload.name}" successfully uploaded')

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error uploading datamodel: {error_message}")

    except Exception as exc:
        logger.exception(f"Error uploading datamodel: {str(exc)}")

    return False


def datamodel_download(
    datamodel_name: str, datamodel_version: str, output_dir: str, client: Client = None
) -> Optional[ICDPayloadHelper]:
    """
    Download the datamodel corresponding to the provided datamodel id into the provided output dir.

    :param datamodel_name: the name of the datamodel to download.
    :param datamodel_version: the version of the datamodel to download.
    :param output_dir: the path into which the datamodel should be downloaded.
    :param client: the Kelvin SDK Client object used to download the datamodel.

    :return: a boolean indicating the end of the datamodel download operation.

    """
    try:
        _client: Client
        if not client:
            _client = login_client_on_current_url()
        else:
            _client = client

        full_datamodel_name = f"{datamodel_name.strip()}:{datamodel_version.strip()}".strip()

        logger.info(f'Downloading datamodel "{full_datamodel_name}"')

        # 1 - retrieve the datamodel and write it
        datamodel: DataModel = _client.data_model.get_data_model(
            data_model_name=datamodel_name, data_model_version=datamodel_version
        )
        # 2 - Despite the ICD definition being mandatory, its model states it is
        if datamodel.icd:
            # 3 - datamodel path and structure
            icd_payload_helper = ICDPayloadHelper(**datamodel.icd)
            output_path = KPath(output_dir) if output_dir else KPath("")
            output_path.create_dir()
            datamodel_path: KPath = output_path / icd_payload_helper.datamodel_file_name

            datamodel_path.write_yaml(yaml_data=icd_payload_helper.dict(exclude_none=True))
            message = f'Datamodel "{full_datamodel_name}" successfully downloaded to "{datamodel_path}"'
            logger.relevant(message)
            return icd_payload_helper

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error downloading datamodel: {error_message}")

    except Exception as exc:
        logger.exception(f"Error downloading datamodel: {str(exc)}")

    return None
