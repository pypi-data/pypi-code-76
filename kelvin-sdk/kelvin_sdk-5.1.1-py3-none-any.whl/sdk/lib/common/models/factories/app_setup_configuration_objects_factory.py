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

import pathlib
from typing import Dict, List, Optional

from kelvin.sdk.cli.version import version
from kelvin.sdk.lib.common.auth.auth_manager import refresh_metadata
from kelvin.sdk.lib.common.configs.internal.docker_configs import DockerConfigs
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.exceptions import InvalidApplicationConfiguration
from kelvin.sdk.lib.common.models.apps.bundle_app import BundleAppType
from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationLanguage, Core, KelvinAppType
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.common.models.apps.ksdk_app_setup import (
    AppCreationObject,
    AppCreationParametersObject,
    BaseAppBuildingObject,
    BundleAppBuildingObject,
    File,
    KelvinAppBuildingObject,
    LegacyAppBuildingObjectLegacy,
    TemplateFile,
)
from kelvin.sdk.lib.common.models.factories.global_configurations_objects_factory import get_global_ksdk_configuration
from kelvin.sdk.lib.common.models.generic import KPath
from kelvin.sdk.lib.common.models.ksdk_global_configuration import KelvinSDKGlobalConfiguration, SDKMetadataEntry
from kelvin.sdk.lib.common.models.legacy.ksdk_app_configuration import LegacyAppGlobalConfiguration
from kelvin.sdk.lib.common.models.types import FileType
from kelvin.sdk.lib.common.schema.schema_manager import generate_base_schema_template
from kelvin.sdk.lib.common.templates.templates_manager import get_app_templates
from kelvin.sdk.lib.common.utils.general_utils import (
    check_if_image_is_allowed_on_platform,
    dict_to_yaml,
    standardize_string,
)
from kelvin.sdk.lib.common.utils.pypi_utils import get_pypi_credentials


# Creation
def get_kelvin_app_creation_object(app_creation_parameters: AppCreationParametersObject) -> AppCreationObject:
    """
    Creates a AppCreationObject from the specified parameters.
    This object will encapsulate all the necessary variables for the creation of an application, thus resulting in
    reduced and more testable code.

    :param app_creation_parameters: the object containing all the required variables for App creation.

    :return: a AppCreationObject containing all the necessary variables for the creation of the application.

    """

    app_name = app_creation_parameters.app_name
    dir_path = app_creation_parameters.app_dir
    app_type = app_creation_parameters.app_type
    kelvin_app_lang = app_creation_parameters.kelvin_app_lang
    kelvin_app_interface = app_creation_parameters.kelvin_app_interface
    kelvin_app_flavour = app_creation_parameters.kelvin_app_flavour

    app_config_file = GeneralConfigs.default_app_config_file
    app_file_system_name = standardize_string(value=app_name)

    app_root_dir_path: KPath = KPath(dir_path) / app_name
    app_source_dir_path: KPath = app_root_dir_path / app_file_system_name
    app_file_path: KPath = app_source_dir_path / f"{app_file_system_name}{kelvin_app_lang.get_extension()}"

    relative_source_app_file_path: KPath = app_file_path.relative_to(app_root_dir_path)
    app_entry_point = str(pathlib.PurePosixPath(relative_source_app_file_path)).replace(".cpp", ".so")

    # 1 - Configuration files, app dir and files
    parameters: dict = {
        "current_sdk_version": version,
        "app_name": app_name,
        "app_title": app_name,
        "app_lang": kelvin_app_lang.value,
        "app_description": GeneralConfigs.default_app_description,
        "app_version": GeneralConfigs.default_app_version,
        "app_file_system_name": app_file_system_name,
        "app_lang_extension": kelvin_app_lang.get_extension(),
        "app_type": app_type.value,
        "kelvin_app_interface": kelvin_app_interface.value if kelvin_app_interface else None,
        "kelvin_app_lang": kelvin_app_lang.value,
        "kelvin_app_flavour": kelvin_app_flavour.value if kelvin_app_flavour else None,
        "cpp_app_header_extension": ".h",
        "app_entry_point": app_entry_point,
        "app_config_file": app_config_file,
    }

    # 2 - Setup the base paths for each app sub folder in the app
    build_dir_path = app_root_dir_path / GeneralConfigs.default_build_dir
    data_dir_path: KPath = app_root_dir_path / GeneralConfigs.default_data_dir
    datamodel_dir_path: KPath = app_root_dir_path / GeneralConfigs.default_datamodel_dir
    docs_dir_path = app_root_dir_path / GeneralConfigs.default_docs_dir
    shared_dir_path = app_root_dir_path / GeneralConfigs.default_shared_dir
    tests_dir_path = app_root_dir_path / GeneralConfigs.default_tests_dir

    # 2 - Retrieve the templates for the files of each folder
    configuration_files_templates: List[TemplateFile] = get_app_templates(
        app_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        kelvin_app_flavour=kelvin_app_flavour,
        file_type=FileType.CONFIGURATION,
    )

    application_files_templates: List[TemplateFile] = get_app_templates(
        app_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        kelvin_app_flavour=kelvin_app_flavour,
        file_type=FileType.APP,
    )

    data_files_templates: List[TemplateFile] = get_app_templates(
        app_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        kelvin_app_flavour=kelvin_app_flavour,
        file_type=FileType.DATA,
    )

    datamodel_files_templates: List[TemplateFile] = get_app_templates(
        app_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        kelvin_app_flavour=kelvin_app_flavour,
        file_type=FileType.DATAMODEL,
    )

    docs_files_templates: List[TemplateFile] = get_app_templates(
        app_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        kelvin_app_flavour=kelvin_app_flavour,
        file_type=FileType.DOCS,
    )

    test_files_templates: List[TemplateFile] = get_app_templates(
        app_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        kelvin_app_flavour=kelvin_app_flavour,
        file_type=FileType.TESTS,
    )

    shared_files_templates: List[TemplateFile] = get_app_templates(
        app_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
        kelvin_app_interface=kelvin_app_interface,
        kelvin_app_flavour=kelvin_app_flavour,
        file_type=FileType.SHARED,
    )

    # 3 - Render the templates and produce File objects for each template
    configuration_files: List[File] = get_files_from_templates(
        directory=app_root_dir_path, templates=configuration_files_templates, render_params=parameters
    )

    app_config_file_path: KPath = app_root_dir_path / app_config_file
    app_configuration = generate_base_schema_template(app_creation_parameters_object=app_creation_parameters)
    app_configuration_yaml: str = dict_to_yaml(content=app_configuration)
    configuration_files.append(File(file=app_config_file_path, content=app_configuration_yaml))

    application_files: List[File] = get_files_from_templates(
        directory=app_source_dir_path, templates=application_files_templates, render_params=parameters
    )

    data_dir_path_files: List[File] = get_files_from_templates(
        directory=data_dir_path, templates=data_files_templates, render_params={}
    )

    docs_dir_path_files: List[File] = get_files_from_templates(
        directory=docs_dir_path, templates=docs_files_templates, render_params={}
    )

    datamodel_dir_path_files: List[File] = get_files_from_templates(
        directory=datamodel_dir_path, templates=datamodel_files_templates, render_params={}
    )

    test_dir_path_files: List[File] = get_files_from_templates(
        directory=tests_dir_path, templates=test_files_templates, render_params=parameters
    )

    shared_dir_path_files: List[File] = get_files_from_templates(
        directory=shared_dir_path, templates=shared_files_templates, render_params=parameters
    )

    # 4 - Include all the file templates into their respective folders
    app_root_dir_object: dict = {"directory": app_root_dir_path, "files": configuration_files}
    app_dir_object: dict = {"directory": app_source_dir_path, "files": application_files}
    build_dir_object: dict = {"directory": build_dir_path}
    data_dir_object: dict = {"directory": data_dir_path, "files": data_dir_path_files}
    datamodel_dir_object: dict = {"directory": datamodel_dir_path, "files": datamodel_dir_path_files}
    docs_dir_object: dict = {"directory": docs_dir_path, "files": docs_dir_path_files}
    shared_dir_object: dict = {"directory": shared_dir_path, "files": shared_dir_path_files}
    tests_dir_object: dict = {"directory": tests_dir_path, "files": test_dir_path_files}

    # 5 - build the final AppCreationObject
    return AppCreationObject(
        **{
            "app_root_dir": app_root_dir_object,
            "app_dir": app_dir_object,
            "build_dir": build_dir_object,
            "data_dir": data_dir_object,
            "datamodel_dir": datamodel_dir_object,
            "docs_dir": docs_dir_object,
            "shared_dir": shared_dir_object,
            "tests_dir": tests_dir_object,
        }
    )


def get_bundle_app_creation_object(app_creation_parameters: AppCreationParametersObject) -> AppCreationObject:
    """
    Creates a AppCreationObject from the specified parameters.
    This object will encapsulate all the necessary variables for the creation of an application, thus resulting in
    reduced and more testable code.

    :param app_creation_parameters: the object containing all the required variables for App creation.

    :return: a AppCreationObject containing all the necessary variables for the creation of the bundle.

    """

    return AppCreationObject.parse_obj(
        {
            k: v if v is not None and v.files else None
            for k, v in get_kelvin_app_creation_object(app_creation_parameters)
        }
    )


def get_docker_app_creation_object(app_creation_parameters: AppCreationParametersObject) -> AppCreationObject:
    """
    Creates a AppCreationObject from the specified parameters.
    This object will encapsulate all the necessary variables for the creation of an application, thus resulting in
    reduced and more testable code.

    :param app_creation_parameters: the object containing all the required variables for App creation.

    :return: a AppCreationObject containing all the necessary variables for the creation of the application.

    """
    # Setup variables
    app_name = app_creation_parameters.app_name
    app_description = app_creation_parameters.app_description
    dir_path = app_creation_parameters.app_dir

    app_config_file = GeneralConfigs.default_app_config_file

    app_root_dir_path: KPath = KPath(dir_path) / app_name

    # 1 - Configuration files, app dir and files
    parameters: dict = {
        "current_sdk_version": version,
        "app_name": app_name,
        "app_description": app_description,
        "app_version": GeneralConfigs.default_app_version,
        "app_config_file": app_config_file,
    }

    # 2 - Retrieve the templates for the files of each folder
    configuration_files_templates: List[TemplateFile] = get_app_templates(
        app_type=app_creation_parameters.app_type,
        kelvin_app_lang=app_creation_parameters.kelvin_app_lang,
        kelvin_app_interface=app_creation_parameters.kelvin_app_interface,
        kelvin_app_flavour=app_creation_parameters.kelvin_app_flavour,
        file_type=FileType.CONFIGURATION,
    )

    # 3 - Render the templates and produce File objects for each template
    configuration_files: List[File] = get_files_from_templates(
        directory=app_root_dir_path, templates=configuration_files_templates, render_params=parameters
    )

    app_config_file_path: KPath = app_root_dir_path / app_config_file
    app_configuration = generate_base_schema_template(app_creation_parameters_object=app_creation_parameters)
    app_configuration_yaml: str = dict_to_yaml(content=app_configuration)
    configuration_files.append(File(file=app_config_file_path, content=app_configuration_yaml))

    # 4 - Include all the file templates into their respective folders
    app_root_dir_object: dict = {"directory": app_root_dir_path, "files": configuration_files}

    # 5 - build the final AppCreationObject
    return AppCreationObject(
        **{
            "app_root_dir": app_root_dir_object,
        }
    )


def get_files_from_templates(directory: KPath, templates: List[TemplateFile], render_params: Dict) -> List[File]:
    """
    When provided with a directory, a list of templates and additional parameters, render the templates with the render
    parameters and create File objects with the associated directory.

    :param directory: the directory to associate to each new File object.
    :param templates: the templates to render.
    :param render_params: the parameters to render the templates with.

    :return: a list of File objects
    """
    files_return_result = []

    for template in templates:
        render_params = render_params or {}
        file_name = template.name.format_map(render_params) if render_params else template.name
        file_content = template.content.render(render_params)
        file_path = directory / file_name
        files_return_result.append(File(file=file_path, content=file_content, **template.options))

    return files_return_result


# Packaging - Apps
def get_legacy_app_building_object(app_dir: str, build_for_upload: bool = False) -> LegacyAppBuildingObjectLegacy:
    """
    Creates a KSDAppBuildingObject from the specified parameters.

    This object will encapsulate all the necessary variables for the building of a App application, thus resulting
    in reduced, cleaner and more testable code.

    :param app_dir: the path to the application's dir.
    :param build_for_upload: indicates whether or the package object aims for an upload.

    :return: a KSDAppBuildingObject containing all the necessary variables for the building of a App.

    """
    # 1 - building a temp dir to copy the files into
    app_config_file: str = GeneralConfigs.default_app_config_file
    dockerfile: str = GeneralConfigs.default_dockerfile
    requirements_file: str = GeneralConfigs.default_requirements_file
    system_packages_file: str = GeneralConfigs.default_system_packages_file
    build_dir: str = GeneralConfigs.default_build_dir
    datamodel_dir: str = GeneralConfigs.default_datamodel_dir

    app_dir_path: KPath = KPath(app_dir)
    app_datamodel_dir_path: KPath = app_dir_path / datamodel_dir
    app_build_dir_path: KPath = app_dir_path / build_dir
    app_config_file_path: KPath = app_dir_path / app_config_file
    system_packages_file_path: KPath = app_dir_path / system_packages_file
    app_config_model = LegacyAppGlobalConfiguration(**app_config_file_path.read_yaml())
    app_name = app_config_model.info.name
    dockerfile_path: KPath = app_build_dir_path / dockerfile

    docker_image_name = app_name
    docker_image_version = app_config_model.info.version
    docker_image_labels = DockerConfigs.ksdk_app_identification_label
    docker_image_labels["name"] = app_name

    build_args = {}
    build_args.update(get_pypi_credentials())

    app_building_object: dict = {
        "fresh_build": build_for_upload,  # The upload is also a 'fresh builds'
        "build_for_upload": build_for_upload,
        # docker
        "dockerfile_path": dockerfile_path,
        "docker_build_context_path": app_dir_path,
        "docker_image_name": docker_image_name,
        "docker_image_version": docker_image_version,
        "docker_image_labels": docker_image_labels,
        "build_args": build_args,
        # app
        "app_config_file_path": app_config_file_path,
        "app_config_model": app_config_model,
        "app_dir_path": app_dir_path,
        "app_build_dir_path": app_build_dir_path,
        "app_datamodel_dir_path": app_datamodel_dir_path,
        # files
        "requirements_file": requirements_file,
        "system_packages_file_path": system_packages_file_path,
    }
    return LegacyAppBuildingObjectLegacy(**app_building_object)


def get_base_app_building_object(app_dir: str, fresh_build: bool = False) -> BaseAppBuildingObject:
    """
    Create a BaseAppBuildingObject from the provided app directory.

    This object will encapsulate all the necessary variables for the building of a base application, thus resulting
    in reduced, cleaner and more testable code.

    :param app_dir: the path to the application's dir.
    :param fresh_build: If specified will remove any cache and rebuild the application from scratch.

    :return: a BaseAppBuildingObject containing all the necessary variables for the building of a base app.

    """
    app_dir_path: KPath = KPath(app_dir)
    app_config_file_path: KPath = app_dir_path / GeneralConfigs.default_app_config_file
    app_build_dir_path: KPath = app_dir_path / GeneralConfigs.default_build_dir
    app_config_raw = app_config_file_path.read_yaml()
    app_config_model = KelvinAppConfiguration(**app_config_raw)
    docker_image_labels = DockerConfigs.ksdk_app_identification_label
    docker_image_name = str(app_config_model.info.name)
    docker_image_labels["name"] = docker_image_name
    base_app_build_object = BaseAppBuildingObject(
        # base building object
        fresh_build=fresh_build,
        app_config_file_path=app_config_file_path,
        app_config_raw=app_config_raw,
        app_config_model=app_config_model,
        app_dir_path=app_dir_path,
        app_build_dir_path=app_build_dir_path,
        docker_image_labels=docker_image_labels,
        docker_image_name=docker_image_name,
    )
    return base_app_build_object


def get_kelvin_app_building_object(
    app_dir: str, fresh_build: bool = False, build_for_upload: bool = False, upload_datamodels: bool = False
) -> KelvinAppBuildingObject:
    """
    Creates a KelvinAppBuildingObject from the specified parameters.

    This object will encapsulate all the necessary variables for the building of a kelvin application, thus resulting
    in reduced, cleaner and more testable code.

    :param app_dir: the path to the application's dir.
    :param fresh_build: If specified will remove any cache and rebuild the application from scratch.
    :param build_for_upload: indicates whether or the package object aims for an upload.
    :param upload_datamodels: If specified, will upload locally defined datamodels.

    :return: a KelvinAppBuildingObject containing all the necessary variables for the building of a kelvin application.

    """
    # 1 - building a temp dir to copy the files into
    app_dir_path: KPath = KPath(app_dir)
    app_build_dir_path: KPath = app_dir_path / GeneralConfigs.default_build_dir
    app_datamodel_dir_path: KPath = app_build_dir_path / GeneralConfigs.default_datamodel_dir
    app_config_file_path: KPath = app_dir_path / GeneralConfigs.default_app_config_file
    app_config_raw = app_config_file_path.read_yaml()
    app_config_model = KelvinAppConfiguration(**app_config_raw)
    app_name = str(app_config_model.info.name)
    app_version = str(app_config_model.info.version)
    dockerfile_path: KPath = app_build_dir_path / GeneralConfigs.default_dockerfile

    kelvin_app_object: Optional[KelvinAppType] = app_config_model.app.kelvin
    if not kelvin_app_object:
        raise InvalidApplicationConfiguration()

    kelvin_app_core_object: Optional[Core] = kelvin_app_object.core
    if not kelvin_app_core_object:
        raise InvalidApplicationConfiguration()

    app_lang = ApplicationLanguage(kelvin_app_core_object.language.type)

    # Retrieve the metadata
    global_ksdk_configuration: KelvinSDKGlobalConfiguration = get_global_ksdk_configuration()
    metadata_sdk_config: Optional[SDKMetadataEntry]
    registry_url: Optional[str]
    try:
        refresh_metadata()
        site_metadata = global_ksdk_configuration.get_metadata_for_url()
        registry_url = site_metadata.docker.full_docker_registry_url
        metadata_sdk_config = site_metadata.sdk
    except ValueError:
        metadata_sdk_config = None
        registry_url = None

    # Setup the images
    base_data_model_builder_image: Optional[str] = None
    base_image: Optional[str] = None
    if kelvin_app_object.images:
        base_data_model_builder_image = kelvin_app_object.images.builder
        base_image = kelvin_app_object.images.base
    if not base_data_model_builder_image and metadata_sdk_config:
        base_data_model_builder_image = metadata_sdk_config.base_data_model_builder_image
    if not base_image and metadata_sdk_config:
        base_image = metadata_sdk_config.get_docker_image_for_lang(app_lang=app_lang)
    # Stop the process from going any further
    if not base_data_model_builder_image:
        raise ValueError(
            """No data model builder image provided.

            1) Please login on a valid platform to retrieve the recommended version,
            or
            2) Provide one in the app.yaml under \"core -> images -> builder\".
            
        """
        )
    if not base_image:
        raise ValueError(
            """No base image provided.

            1) Please login on a valid platform to retrieve the recommended version,
            or
            2) Provide one in the app.yaml under \"core -> images -> base\".
            
        """
        )

    check_if_image_is_allowed_on_platform(registry_url=registry_url, docker_image_name=base_data_model_builder_image)
    check_if_image_is_allowed_on_platform(registry_url=registry_url, docker_image_name=base_image)

    docker_image_name = app_name
    docker_image_version = app_version
    docker_image_labels = DockerConfigs.ksdk_app_identification_label
    docker_image_labels["name"] = app_name

    build_args = {}
    build_args.update(get_pypi_credentials())

    return KelvinAppBuildingObject(
        # base building object
        fresh_build=fresh_build,
        build_for_upload=build_for_upload,
        upload_datamodels=upload_datamodels,
        app_config_file_path=app_config_file_path,
        app_config_raw=app_config_raw,
        app_config_model=app_config_model,
        app_dir_path=app_dir_path,
        app_build_dir_path=app_build_dir_path,
        docker_image_labels=docker_image_labels,
        docker_image_name=docker_image_name,
        # kelvin app building object
        dockerfile_path=dockerfile_path,
        docker_build_context_path=app_dir_path,
        base_image=base_image,
        base_data_model_builder_image=base_data_model_builder_image,
        docker_image_version=docker_image_version,
        build_args=build_args,
        app_datamodel_dir_path=app_datamodel_dir_path,
    )


def get_bundle_app_building_object(
    app_dir: str,
    fresh_build: bool = False,
    build_for_upload: bool = False,
) -> BundleAppBuildingObject:
    """
    Creates a BundleAppBuildingObject from the specified parameters.

    This object will encapsulate all the necessary variables for the building of a bundle application, thus resulting
    in reduced, cleaner and more testable code.

    :param app_dir: the path to the application's dir.
    :param fresh_build: If specified will remove any cache and rebuild the application from scratch.
    :param build_for_upload: indicates whether or the package object aims for an upload.

    :return: a BundleAppBuildingObject containing all the necessary variables for the building of a bundle application.

    """

    # 1 - building a temp dir to copy the files into
    app_dir_path: KPath = KPath(app_dir)
    app_build_dir_path: KPath = app_dir_path / GeneralConfigs.default_build_dir
    app_datamodel_dir_path: KPath = app_build_dir_path / GeneralConfigs.default_datamodel_dir
    app_config_file_path: KPath = app_dir_path / GeneralConfigs.default_app_config_file
    app_config_raw = app_config_file_path.read_yaml()
    app_config_model = KelvinAppConfiguration(**app_config_raw)
    app_name = str(app_config_model.info.name)
    app_version = str(app_config_model.info.version)
    dockerfile_path: KPath = app_build_dir_path / GeneralConfigs.default_dockerfile

    bundle_app_object: Optional[BundleAppType] = app_config_model.app.bundle
    if bundle_app_object is None or not bundle_app_object.pipelines:
        raise InvalidApplicationConfiguration()

    # Retrieve the metadata
    global_ksdk_configuration: KelvinSDKGlobalConfiguration = get_global_ksdk_configuration()
    metadata_sdk_config: Optional[SDKMetadataEntry]
    registry_url: Optional[str]
    try:
        site_metadata = global_ksdk_configuration.get_metadata_for_url()
        registry_url = site_metadata.docker.full_docker_registry_url
        metadata_sdk_config = site_metadata.sdk
    except ValueError:
        metadata_sdk_config = None
        registry_url = None

    # Setup the images
    base_data_model_builder_image: Optional[str] = None
    base_image: Optional[str] = None
    if bundle_app_object.images:
        base_data_model_builder_image = bundle_app_object.images.builder
        base_image = bundle_app_object.images.base
    if not base_data_model_builder_image and metadata_sdk_config:
        base_data_model_builder_image = metadata_sdk_config.base_data_model_builder_image
    if not base_image and metadata_sdk_config:
        base_image = metadata_sdk_config.get_docker_image_for_lang()

    # Stop the process from going any further
    if not base_data_model_builder_image:
        raise ValueError(
            """No data model builder image provided.

            1) Please login on a valid platform to retrieve the recommended version,
            or
            2) Provide one in the app.yaml under \"core -> images -> builder\".
            
        """
        )
    if not base_image:
        raise ValueError(
            """No base image provided.

            1) Please login on a valid platform to retrieve the recommended version,
            or
            2) Provide one in the app.yaml under \"core -> images -> base\".
            
        """
        )

    check_if_image_is_allowed_on_platform(registry_url=registry_url, docker_image_name=base_data_model_builder_image)
    check_if_image_is_allowed_on_platform(registry_url=registry_url, docker_image_name=base_image)

    docker_image_name = app_name
    docker_image_version = app_version
    docker_image_labels = DockerConfigs.ksdk_app_identification_label
    docker_image_labels["name"] = app_name

    build_args = {}
    build_args.update(get_pypi_credentials())

    return BundleAppBuildingObject(
        # base building object
        fresh_build=fresh_build,
        build_for_upload=build_for_upload,
        app_config_file_path=app_config_file_path,
        app_config_raw=app_config_raw,
        app_config_model=app_config_model,
        app_dir_path=app_dir_path,
        app_build_dir_path=app_build_dir_path,
        docker_image_labels=docker_image_labels,
        docker_image_name=docker_image_name,
        # kelvin app building object
        dockerfile_path=dockerfile_path,
        docker_build_context_path=app_dir_path,
        base_image=base_image,
        base_data_model_builder_image=base_data_model_builder_image,
        docker_image_version=docker_image_version,
        build_args=build_args,
        app_datamodel_dir_path=app_datamodel_dir_path,
    )


def get_default_app_configuration(
    app_dir_path: Optional[KPath] = None, app_config_file_path: Optional[KPath] = None
) -> KelvinAppConfiguration:
    """
    Retrieve the application's configuration from either the provided app directory of app configuration.

    :param app_dir_path: the path to the application's directory.
    :param app_config_file_path: the path to the application's configuration.

    :return: a KelvinAppConfiguration object matching the app configuration of the app.

    """
    if app_config_file_path:
        return KelvinAppConfiguration(**app_config_file_path.read_yaml())

    app_config_file_path_aux = KPath(GeneralConfigs.default_app_config_file)

    if app_dir_path:
        app_config_file_path_aux = app_dir_path / app_config_file_path

    return KelvinAppConfiguration(**app_config_file_path_aux.read_yaml())


def get_default_app_name(app_dir_path: Optional[KPath] = None) -> str:
    """
    Retrieve the app name from the default configuration file (usually, app.yaml)

    :param app_dir_path: the path to the application's directory.

    :return: a string  containing the default app name.

    """
    app_configuration = get_default_app_configuration(app_dir_path=app_dir_path)

    return app_configuration.info.app_name_with_version
