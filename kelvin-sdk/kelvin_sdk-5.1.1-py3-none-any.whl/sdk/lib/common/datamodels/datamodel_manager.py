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

from typing import Dict, Generator, List, Optional, Tuple, Type

from kelvin.sdk.client import Client
from kelvin.sdk.lib.common.api.datamodel import datamodel_download, datamodel_list, datamodel_upload
from kelvin.sdk.lib.common.auth.auth_manager import login_client_on_current_url
from kelvin.sdk.lib.common.configs.internal.datamodel_configs import DatamodelConfigs
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.exceptions import DataModelException
from kelvin.sdk.lib.common.models.apps.kelvin_app import DataModel
from kelvin.sdk.lib.common.models.apps.ksdk_app_setup import KelvinAppBuildingObject
from kelvin.sdk.lib.common.models.datamodels import ICDPayloadHelper
from kelvin.sdk.lib.common.models.factories.app_setup_configuration_objects_factory import get_base_app_building_object
from kelvin.sdk.lib.common.models.generic import KPath
from kelvin.sdk.lib.common.models.types import EmbeddedFiles
from kelvin.sdk.lib.common.templates.templates_manager import get_embedded_file
from kelvin.sdk.lib.common.utils.display_utils import display_yes_or_no_question
from kelvin.sdk.lib.common.utils.general_utils import get_files_from_dir, unique_items
from kelvin.sdk.lib.common.utils.logger_utils import logger


# 1 - App Building
def setup_datamodels(kelvin_app_building_object: KelvinAppBuildingObject) -> Optional[KPath]:
    """
    Handle the datamodels, both the raw datamodel folder and app configuration datamodel specifications and copy them
    to the intended build dir folder for processing.

    :param kelvin_app_building_object: the LegacyAppBuildingObjectLegacy used to configure the datamodel interaction.

    :return: an optional string indicating the path to the build folder that will contain the models to be compiled.

    """
    logger.info("Processing application data models..")

    datamodel_dir_path = kelvin_app_building_object.app_datamodel_dir_path
    if datamodel_dir_path is None:
        return None

    kelvin_app_configuration = kelvin_app_building_object.app_config_model.app.kelvin
    app_name = kelvin_app_building_object.app_config_model.info.name
    if kelvin_app_configuration and kelvin_app_configuration.core:
        datamodels_to_handle = kelvin_app_configuration.core.data_models
        datamodel_dir_path.delete_dir().create_dir()
        if datamodels_to_handle:
            logger.info(f'Retrieving data models for "{app_name}"')
            client = login_client_on_current_url()
            if kelvin_app_building_object.build_for_upload:
                _handle_upload_phase_datamodels(
                    datamodels_to_handle=datamodels_to_handle,
                    input_dir_path=KPath(datamodel_dir_path.name),
                    ignore_warning=kelvin_app_building_object.upload_datamodels,
                )
            for datamodel in datamodels_to_handle:
                if datamodel.path:  # local
                    datamodel_path: KPath = KPath(datamodel.path)
                    ICDPayloadHelper(**datamodel_path.read_yaml())
                    datamodel_path.clone_into(path=datamodel_dir_path)
                else:  # remote
                    download_datamodel(
                        client=client,
                        datamodel_name=str(datamodel.name),
                        datamodel_version=str(datamodel.version),
                        output_dir=datamodel_dir_path,
                    )

            content = [content for content in datamodel_dir_path.dir_content() if not content.startswith(".")]
            should_compile = bool(content)
            return datamodel_dir_path if should_compile else None

    logger.info("No data models to process")
    return None


# 2 - Datamodel creation
def create_datamodel(datamodel_name: str, output_dir: Optional[str]) -> bool:
    """
    Creates a datamodel from the specified parameters.

    :param datamodel_name: the name of the datamodel to create.
    :param output_dir: the output directory where the datamodel will be created.

    :return: a boolean indicating whether the datamodel was successfully created..

    """

    try:
        # 1 - check if the current output directory is an app.
        if not output_dir:
            try:
                base_build_object = get_base_app_building_object(app_dir="")
                output_dir = base_build_object.app_dir_path / GeneralConfigs.default_datamodel_dir
            except Exception:
                raise DataModelException("Please provide a valid application directory or specify an output directory")

        # 2 - Validate the datamodel name and determine its file path
        datamodel_item = ICDPayloadHelper(
            name=datamodel_name,
            version=DatamodelConfigs.datamodel_default_version,
            description="",
            payload_fields=[],
            class_name="SomeClassName",  # this is not used
        )
        datamodel_file_name = datamodel_item.datamodel_file_name

        logger.info(f'Creating spec for data model "{datamodel_item.name}"')

        # 3 - Render the default ICD sample template
        default_icd_template = get_embedded_file(embedded_file=EmbeddedFiles.DEFAULT_DATAMODEL_TEMPLATE)
        default_icd_template_rendered = default_icd_template.render(
            datamodel_name=datamodel_item.name, datamodel_version=datamodel_item.version
        )

        # 4 - Write it down on the target file
        template_output_file_path: KPath = KPath(output_dir) / datamodel_file_name
        template_output_file_path.write_content(content=default_icd_template_rendered)

        # 5 - Log the success message
        output_file: str = str(template_output_file_path.absolute())
        logger.relevant(f'Data model "{datamodel_name}" spec successfully created in "{output_file}"')
        return True

    except Exception as exc:
        logger.exception(f"Error creating data model spec file: {str(exc)}")
        return False


# 3 - Datamodel upload
def upload_datamodels(input_dir: Optional[str], datamodels: Optional[List[str]]) -> bool:
    """

    Upload all the datamodels in the provided input directory.

    :param input_dir: the directory to read all the data models from.
    :param datamodels: the names of the datamodels to upload.

    :return: a boolean indicating the end of the datamodel upload operation.

    """
    try:
        # auxiliary variable due to mypy issue with optional str
        datamodels_input_dir: str
        if not input_dir:
            try:
                base_build_object = get_base_app_building_object(app_dir="")
                datamodels_input_dir = base_build_object.app_dir_path / GeneralConfigs.default_datamodel_dir
            except Exception:
                raise DataModelException("Please provide a valid application directory or specify an input directory")
        else:
            datamodels_input_dir = input_dir

        logger.info(f'Uploading data models from directory "{datamodels_input_dir}"')

        loaded_datamodels = _load_all_datamodel_files(input_dir=datamodels_input_dir)
        if datamodels:
            loaded_datamodels = _filter_datamodels(loaded_datamodels=loaded_datamodels, datamodel_names=datamodels)
        if loaded_datamodels:
            all_platform_datamodels = datamodel_list(all_datamodels=True, should_display=False)
            all_datamodels = [item for item in all_platform_datamodels[0].raw_data if all_platform_datamodels]
            dependency_tree = _build_datamodel_upload_dependency_tree(loaded_datamodels=loaded_datamodels)
            upload_result = _process_datamodel_upload_dependency_tree(
                all_platform_datamodels=all_datamodels,
                loaded_datamodels=loaded_datamodels,
                dependency_tree=dependency_tree,
            )
            logger.relevant("Data models successfully processed")
            return upload_result
        else:
            logger.error("No data models to process matching your criteria")
            return False
    except Exception as exc:
        logger.exception(f"Error uploading data models: {str(exc)}")
        return False


# 4 - Datamodel download
def download_datamodel(
    datamodel_name: str, datamodel_version: str, output_dir: Optional[str], client: Client = None
) -> bool:
    """
    Download the datamodel corresponding to the provided datamodel id into the provided output dir.

    :param datamodel_name: the name of the datamodel to download.
    :param datamodel_version: the version of the datamodel to download.
    :param output_dir: the path into which the datamodel should be downloaded.
    :param client: the Kelvin SDK Client object used to download the datamodel.

    :return: a boolean indicating the end of the datamodel download operation.

    """

    datamodel_output_dir: str
    if not output_dir:
        try:
            base_build_object = get_base_app_building_object(app_dir="")
            datamodel_output_dir = base_build_object.app_dir_path / GeneralConfigs.default_datamodel_dir
        except Exception:
            raise DataModelException("Please provide a valid application directory or specify an output directory")
    else:
        datamodel_output_dir = output_dir

    acquired_datamodel: Optional[ICDPayloadHelper] = datamodel_download(
        datamodel_name=datamodel_name,
        datamodel_version=datamodel_version,
        output_dir=datamodel_output_dir,
        client=client,
    )
    if acquired_datamodel:
        downloaded_datamodel_fields = acquired_datamodel.dependency_datamodels
        for name, version in downloaded_datamodel_fields:
            download_datamodel(
                datamodel_name=name, datamodel_version=version, output_dir=datamodel_output_dir, client=client
            )

    if not acquired_datamodel:
        raise DataModelException("Error processing data model tree")

    return True


# 5 - Compile datamodels
def datamodel_extract_schema(input_dir: str, output_dir: str, datamodels: Optional[List[str]]) -> bool:
    """
    Extract the schema of the provided data models.

    :param input_dir: the directory to read the data models from.
    :param output_dir: the directory to output the schemas of the datamodels.
    :param datamodels: the names of the data models to extract the schema from.

    :return: a boolean indicating the end of the datamodel extraction operation.

    """
    try:
        # auxiliary variable due to mypy issue with optional str
        datamodels_input_dir: str
        if not input_dir:
            try:
                base_build_object = get_base_app_building_object(app_dir="")
                datamodels_input_dir = base_build_object.app_dir_path / GeneralConfigs.default_datamodel_dir
            except Exception:
                raise DataModelException("Please provide a valid application directory or specify an input directory")
        else:
            datamodels_input_dir = input_dir

        logger.info(f'Extracting schemas from data models in directory "{datamodels_input_dir}"')

        loaded_datamodels = _load_all_datamodel_files(input_dir=datamodels_input_dir)
        if datamodels:
            loaded_datamodels = _filter_datamodels(loaded_datamodels=loaded_datamodels, datamodel_names=datamodels)
        if loaded_datamodels:
            from kelvin.icd import ICD, Message
            from kelvin.icd.icd import resolve

            output_dir_path: KPath = KPath(output_dir)
            models: Dict[str, Type[Message]] = {}
            icds: List[ICD] = [
                icd for file_path, datamodel in loaded_datamodels for icd in ICD.from_file(path=file_path)
            ]
            for icd in resolve(icds):
                icd_path = f"{icd.name.replace('.', '_')}.json"
                model = icd.to_model(models=models)
                complete_icd_path: KPath = output_dir_path / icd_path
                complete_icd_path.write_json(model.schema())
            logger.relevant("Data models schemas successfully extracted")
            return True
        else:
            logger.error("No data models to process matching your criteria")
            return False
    except Exception as exc:
        logger.exception(f"Error extract schemas from data models: {str(exc)}")
        return False


# Utils
def _load_all_datamodel_files(input_dir: str) -> List[Tuple[str, ICDPayloadHelper]]:
    """
    Load all datamodels from the provided input directory.

    :param input_dir: the input directory to read the datamodel files from.

    :return: a list of tuples containing the key and the respective ICDPayloadHelper
    """
    logger.info(f'Loading all data model files from directory "{input_dir}"')

    # 1 - get all datamodels
    yml_file_type: str = DatamodelConfigs.datamodel_default_icd_extension
    datamodel_files = get_files_from_dir(file_type=yml_file_type, input_dir=input_dir)
    datamodel_file_paths = [KPath(input_dir) / file for file in datamodel_files]

    # 2 - from the datamodel files, load all datamodel entries into a list of tuples (path + datamodel ICD)
    loaded_datamodels: List = []
    for file in datamodel_file_paths:
        yaml_content: Generator = file.read_yaml_all()
        for entry in yaml_content:
            loaded_datamodels.append((file, ICDPayloadHelper(**entry)))

    # 3 - report and return
    total = len(loaded_datamodels)
    logger.relevant(f'{total} data models loaded from directory "{input_dir}"')
    return loaded_datamodels


def _handle_upload_phase_datamodels(
    datamodels_to_handle: List[DataModel], input_dir_path: KPath, ignore_warning: bool = False
) -> bool:
    """
    If a local datamodel is provided during the appregistry upload phase, make sure to warn the user
    and, if ruled so, upload them.

    Parameters
    ----------
    datamodels_to_handle : the names of the datamodels to handle. Mainly for display purpose.
    input_dir_path : The input directory where the datamodels are hosted.
    ignore_warning: indicates whether the upload warning should be displayed.

    Returns
    -------
    a boolean indicating whether the datamodels have been successfully uploaded.

    """
    local_datamodels = [f"{model.name}:{model.version}" for model in datamodels_to_handle if model.path]

    if local_datamodels:
        local_datamodels_list = ", ".join(local_datamodels)
        local_datamodels_upload_warning: str = f"""
    
            The application you're trying to upload has references to local data models:
    
            > {local_datamodels_list}
    
            Do you wish to upload them to the platform before proceeding?
    
        """
        if not ignore_warning:
            ignore_warning = display_yes_or_no_question(question=local_datamodels_upload_warning)
        if ignore_warning:
            result = upload_datamodels(input_dir=input_dir_path, datamodels=None)
            if not result:
                raise DataModelException()

    return True


def _filter_datamodels(
    loaded_datamodels: List[Tuple[str, ICDPayloadHelper]], datamodel_names: List[str]
) -> List[Tuple[str, ICDPayloadHelper]]:
    """
    Filter the loaded datamodels list

    :param loaded_datamodels: the list of datamodels to process.
    :param datamodel_names: the list of datamodels to filter.

    :return: a list of filtered datamodels tuples
    """

    filtered_datamodels: List[Tuple[str, ICDPayloadHelper]] = []
    filtered_datamodels_names: List[str] = []

    for datamodel in loaded_datamodels:
        file, icd = datamodel
        if icd.full_datamodel_name in datamodel_names:
            filtered_datamodels.append(datamodel)
            filtered_datamodels_names.append(icd.full_datamodel_name)

    # check for not found datamodels
    for datamodel_name in datamodel_names:
        if datamodel_name not in filtered_datamodels_names:
            logger.warn(f'No data model found matching your criteria: "{datamodel_name}"')

    total = len(filtered_datamodels)
    if total:
        logger.relevant(f"A total of {total} data models loaded match your criteria: {filtered_datamodels_names}")

    return filtered_datamodels


def _build_datamodel_upload_dependency_tree(
    loaded_datamodels: List[Tuple[str, ICDPayloadHelper]]
) -> Tuple[List[str], List[str]]:
    """
    Process the loaded datamodels and retrieve the dependency tree with the correct upload structure.

    :param loaded_datamodels: the list of datamodels to process.

    :return: the organized list datamodel names with version, ready to operate.
    """
    logger.info("Processing the data model dependency tree.")
    requires_processing: Dict[str, List[str]] = {}
    prepare_for_upload: List[str] = []

    # 1 - Load the datamodels
    for _, datamodel in loaded_datamodels:
        datamodel_name_with_version = f"{datamodel.name}:{datamodel.version}"
        datamodel_fields = datamodel.payload_fields or []
        has_dependencies: bool = False
        requires_processing[datamodel_name_with_version] = []  # Register the datamodel in the dependency tree
        for field in datamodel_fields:
            # 2 - Custom datamodels must have a semver tag. If not, its a raw sub type and its not processed (go to #4)
            has_dependencies = has_dependencies or bool(field.type and ":" in field.type)
            if has_dependencies and field.type and field.type not in requires_processing[datamodel_name_with_version]:
                # 3 - Register each sub datamodel reference
                requires_processing[datamodel_name_with_version].append(field.type)
        # 4 - if the datamodel has no custom datamodel in its fields, skip any processing and mark it for upload.
        if not has_dependencies:
            prepare_for_upload.append(datamodel_name_with_version)

    verify_on_the_platform = []
    while requires_processing:
        keys = requires_processing.keys()
        items = list(requires_processing.items())
        for key, value in items:
            for item in value:
                if item in keys:
                    prepare_for_upload.append(item)
                else:
                    verify_on_the_platform.append(item)
                prepare_for_upload.append(key)
            del requires_processing[key]

    prepare_for_upload = unique_items(items=prepare_for_upload)
    verify_on_the_platform = unique_items(items=verify_on_the_platform)
    verify_on_the_platform = [item for item in verify_on_the_platform if item not in prepare_for_upload]
    return prepare_for_upload, verify_on_the_platform


def _process_datamodel_upload_dependency_tree(
    all_platform_datamodels: List[DataModel],
    loaded_datamodels: List[Tuple[str, ICDPayloadHelper]],
    dependency_tree: Tuple[List[str], List[str]],
) -> bool:
    """
    Process the datamodel dependency tree and uploaded what is necessary to the platform.

    :param all_platform_datamodels: a list of all platform datamodels.
    :param loaded_datamodels: a list containing all the loaded datamodels.
    :param dependency_tree: the dependency tree composed by the ordered name of datamodels to upload.

    :return: a bool indicating the datamodels were successfully processed.
    """
    logger.info("Initialising the data model upload operation.")

    # 1 - get a list of datamodels as strings
    all_platform_datamodels_names: List[str] = [f"{model.name}:{model.version}" for model in all_platform_datamodels]

    datamodels_to_upload, datamodels_to_check_on_the_platform = dependency_tree
    for datamodel in datamodels_to_check_on_the_platform:
        # 2 - if the datamodel is not present in the platform nor the local definition, raise an exception
        if datamodel not in all_platform_datamodels_names:
            raise DataModelException(message=f'Invalid data model "{datamodel}". Please check the platform')
        else:  # 3 - If the datamodel already exists, inform the user
            logger.warn(f'Data model "{datamodel}" already present in the system. Skipping.')

    for datamodel_name_with_version in datamodels_to_upload:
        if datamodel_name_with_version not in all_platform_datamodels_names:
            name, version = datamodel_name_with_version.split(":")
            clean = [(file, icd) for (file, icd) in loaded_datamodels if icd.name == name and icd.version == version]
            file, icd = next(iter(clean))
            if icd:
                datamodel_uploaded = datamodel_upload(datamodel_content=icd.dict(), source=str(file))
                if not datamodel_uploaded:
                    raise DataModelException("Error processing data model tree")
        else:
            logger.warn(f'Data model "{datamodel_name_with_version}" already present in the system. Skipping.')

    return True
