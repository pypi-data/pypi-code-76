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

from collections import defaultdict
from math import log10
from tempfile import TemporaryDirectory
from typing import DefaultDict, List, Mapping, Optional, Sequence, Set
from urllib.parse import urlparse

from click import Abort
from typing_extensions import Literal

from kelvin.sdk.client.model.responses import AppVersion
from kelvin.sdk.lib.common.apps.apps_migration_manager import migrate_app_configuration
from kelvin.sdk.lib.common.configs.internal.docker_configs import DockerConfigs
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.datamodels.datamodel_manager import setup_datamodels
from kelvin.sdk.lib.common.emulation.emulation_manager import emulation_start
from kelvin.sdk.lib.common.exceptions import AppException, KDockerException, NoApplicationConfigurationProvided
from kelvin.sdk.lib.common.models.apps.bundle_app import Pipeline
from kelvin.sdk.lib.common.models.apps.common import OPCUAEndpoint
from kelvin.sdk.lib.common.models.apps.kelvin_app import (
    IO,
    ApplicationInterface,
    ApplicationLanguage,
    ClientInterfaceType,
    Connection,
    ConnectionType,
    Core,
    DataModel,
    Images,
    Interface,
    Item,
    KelvinAppType,
    Language,
    OPCUAConnectionType,
    PythonLanguageType,
    RegistryMap,
)
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import App, AppType, Info, KelvinAppConfiguration
from kelvin.sdk.lib.common.models.apps.ksdk_app_setup import (
    AppCreationParametersObject,
    ApplicationName,
    BundleAppBuildingObject,
    DockerAppBuildingObject,
    KelvinAppBuildingObject,
)
from kelvin.sdk.lib.common.models.factories.app_setup_configuration_objects_factory import (
    get_base_app_building_object,
    get_bundle_app_building_object,
    get_bundle_app_creation_object,
    get_docker_app_creation_object,
    get_kelvin_app_building_object,
    get_kelvin_app_creation_object,
)
from kelvin.sdk.lib.common.models.factories.docker_manager_factory import get_docker_manager
from kelvin.sdk.lib.common.models.generic import KPath, OSInfo
from kelvin.sdk.lib.common.models.ksdk_docker import DockerImageNameDetails
from kelvin.sdk.lib.common.schema.schema_manager import validate_app_schema_from_app_config_file
from kelvin.sdk.lib.common.utils.application_utils import (
    check_if_app_name_is_valid,
    check_if_app_name_with_version_is_valid,
)
from kelvin.sdk.lib.common.utils.display_utils import display_yes_or_no_question
from kelvin.sdk.lib.common.utils.general_utils import chdir, lower, merge, standardize_string
from kelvin.sdk.lib.common.utils.logger_utils import logger
from kelvin.sdk.lib.common.utils.version_utils import assess_docker_image_version

IOType = Literal["inputs", "outputs", "parameters"]


# 1 - entrypoint functions
def app_create_from_wizard() -> bool:
    """
    The entry point for the creation of a App. (WizardTree version)

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    :return: a bool indicating whether the App creation was successful.

    """
    from kelvin.sdk.lib.common.utils.cli_wizard_utils import start_app_creation_wizard

    try:
        app_creation_parameters = start_app_creation_wizard()
    except Abort:
        return True
    except Exception as exc:
        logger.exception(f"Error processing wizard input parameters: {str(exc)}")
        return False

    return _app_create(app_creation_parameters=app_creation_parameters)


def app_create_from_parameters(
    app_dir: str,
    app_name: Optional[str],
    app_description: Optional[str],
    app_type: Optional[AppType],
    kelvin_app_lang: Optional[ApplicationLanguage],
) -> bool:
    """
    The entry point for the creation of a App. (Parameter version)

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    :param app_dir: the app's targeted dir. Will contain all the application files.
    :param app_name: the name of the new app.
    :param app_description: the description of the new app.
    :param app_type: the type of the new application. # E.g. 'docker', 'kelvin'.
    :param kelvin_app_lang: the language the new app will be written on. For kelvin apps only. # E.g. python.

    :return: a bool indicating whether the App creation was successful.

    """

    from kelvin.sdk.lib.common.models.apps.ksdk_app_setup import AppCreationParametersObject

    try:
        app_creation_parameters = AppCreationParametersObject(
            app_dir=app_dir,
            app_name=app_name,
            app_description=app_description,
            app_type=app_type,
            kelvin_app_lang=kelvin_app_lang,
        )

        return _app_create(app_creation_parameters=app_creation_parameters)
    except Exception as exc:
        app_creation_error_parsing_parameters: str = f"""{str(exc)}.
                \n
                Proceeding with wizard.
        """
        logger.exception(app_creation_error_parsing_parameters)
        return app_create_from_wizard()


def app_build(
    app_dir: str, fresh_build: bool = False, build_for_upload: bool = False, upload_datamodels: bool = False
) -> bool:
    """
    The entry point for the building of an application.

    Attempts to read the application content

    :param app_dir: the path where the application is hosted.
    :param fresh_build: If specified will remove any cache and rebuild the application from scratch.
    :param build_for_upload: indicates whether or the package object aims for an upload.
    :param upload_datamodels: If specified, will upload locally defined datamodels.

    :return: a boolean indicating whether the App was successfully built.

    """
    try:
        logger.info("Assessing basic application info..")

        base_app_building_object = get_base_app_building_object(app_dir=app_dir, fresh_build=fresh_build)

        validate_app_schema_from_app_config_file(app_config=base_app_building_object.app_config_raw)

        app_type = base_app_building_object.app_config_model.app.type
        app_name = base_app_building_object.app_config_model.info.name

        if app_type == AppType.kelvin:
            logger.info(f'Building "Core type" application "{app_name}"')
            kelvin_app_building_object = get_kelvin_app_building_object(
                app_dir=app_dir,
                build_for_upload=build_for_upload,
                upload_datamodels=upload_datamodels,
                fresh_build=fresh_build,
            )
            return _build_kelvin_app(kelvin_app_building_object=kelvin_app_building_object)
        if app_type == AppType.bundle:
            logger.info(f'Building "Core bundle type" application "{app_name}"')
            bundle_app_building_object = get_bundle_app_building_object(
                app_dir=app_dir, build_for_upload=build_for_upload, fresh_build=fresh_build
            )
            return _build_bundle_app(bundle_app_building_object=bundle_app_building_object)
        if app_type == AppType.docker:
            logger.info(f'Building "Docker type" application "{app_name}"')
            docker_app_building_object = DockerAppBuildingObject(**base_app_building_object.dict())
            return _build_docker_app(docker_app_building_object=docker_app_building_object)
        return True
    except Exception as exc:
        error_message = f"""Error building application: {str(exc)}

            Consider building the app in verbose mode to retrieve more information: --verbose
        """
        logger.exception(error_message)
        return False


def app_migrate(app_dir_path: str) -> bool:
    """
    Migrate the application configuration to the new schema version.

    :param app_dir_path: the path to the application that requires migrate.

    :return: a boolean indicating whether the App was successfully migrate.

    """
    try:
        logger.info("Migrating application configuration to the new version.")

        default_migrated_app_config_file = GeneralConfigs.default_migrated_app_config_file
        output_file_path = KPath(app_dir_path) / default_migrated_app_config_file

        migrate_app_configuration(app_dir_path=app_dir_path, output_file_path=output_file_path)

        app_migrate_success: str = f"""Application successfully migrated.
            New configuration successfully output to:
                {output_file_path}
        """
        logger.relevant(app_migrate_success)
        return True

    except Exception as exc:
        logger.exception(f"Error migrating application: {str(exc)}")
        return False


def app_images_unpack(
    app_name_with_version: str,
    output_dir: str,
    image_dir: str = DockerConfigs.app_container_app_dir_path,
    clean_dir: bool = True,
) -> bool:
    """
    Extract the content of an application from its built image.

    :param app_name_with_version: the name of the image to unpack the app from.
    :param output_dir: the output directory to output the application content.
    :param image_dir: the directory from which to extract the application content.
    :param clean_dir: clean the directory before extracting into it.

    :return: a boolean indicating whether the application was successfully unpacked and extracted.

    """

    try:
        image_name_details = DockerImageNameDetails(
            docker_image_name=app_name_with_version, registry_url=app_name_with_version
        )
        app = image_name_details.exclude_registry

        check_if_app_name_with_version_is_valid(app_name_with_version=app)

        application_name = ApplicationName(name=app)

        logger.info(f'Unpacking application "{application_name.full_name}" to directory "{output_dir}"')

        docker_manager = get_docker_manager()

        docker_image_exists = docker_manager.check_if_docker_image_exists(docker_image_name=app_name_with_version)

        if not docker_image_exists:
            raise KDockerException(f'Application "{app_name_with_version}" is not available on the local registry')

        app_was_unpacked = docker_manager.unpack_app_from_docker_image(
            app_name=app_name_with_version, output_dir=output_dir, image_dir=image_dir, clean_dir=clean_dir
        )

        if app_was_unpacked:
            logger.relevant(f'Application "{application_name.full_name}" successfully unpacked to "{output_dir}"')

        return app_was_unpacked

    except Exception as exc:
        logger.exception(f"Error unpacking application: {str(exc)}")
        return False


# 2 - App bundle management
def app_images_remove(app_name_with_version: str) -> bool:
    """
    Remove the specified application from the existing image list.

    :param app_name_with_version: the app to be removed.

    :return: a boolean indicating whether the application was successfully removed.

    """
    try:
        check_if_app_name_with_version_is_valid(app_name_with_version=app_name_with_version)

        application_name = ApplicationName(name=app_name_with_version)

        logger.info(f'Removing packaged application "{application_name.full_name}"')

        docker_manager = get_docker_manager()
        docker_manager.remove_docker_image(docker_image_name=application_name.full_name)

        logger.relevant(f'Successfully removed application: "{application_name.full_name}"')

        return True

    except Exception as exc:
        logger.exception(f"Error removing application: {str(exc)}")
        return False


def app_bundle_list(app_config: str = None) -> Optional[List[str]]:
    """

    List all the applications available in an app bundle.

    Parameters
    ----------
    app_config : The app bundle configuration file to process.

    Returns
    -------
    A list of strings containing both app name and version.
    """
    try:
        # 1 - Load the bundle App Configuration
        app_config_file_path: KPath = KPath(app_config)
        if not app_config_file_path.exists():
            raise NoApplicationConfigurationProvided()
        bundle_app_configuration = KelvinAppConfiguration(**app_config_file_path.read_yaml())

        # 2 - If there is a bundle (it should), list all of its pipelines
        if bundle_app_configuration.app.bundle:
            # 2.1 - Get the application name and version and get its 'full' format.
            bundle_app_name_str: str = str(bundle_app_configuration.info.name)
            bundle_app_version_str: str = str(bundle_app_configuration.info.version)
            bundle_app_name = ApplicationName(name=bundle_app_name_str, version=bundle_app_version_str)
            # 2.2 - Retrieve the pipelines and print each line (if there are any)
            bundle_pipelines = bundle_app_configuration.app.bundle.pipelines
            pipeline_list: List[str] = []
            if bundle_pipelines:
                pipeline_list = [f"{index} - {p.name}:{p.version}" for index, p in enumerate(bundle_pipelines)]
                pipeline_list_str = """\n\t\t""".join(pipeline_list)
                logger.relevant(f'Application pipelines for "{bundle_app_name.full_name}":\n\t\t{pipeline_list_str}')
            # 2.3 - If not, simply yield a warning and return an empty list.
            else:
                logger.warning(f'No application pipelines defined for "{bundle_app_name.full_name}"')
            return pipeline_list
        # 3 - If it is not an application bundle, raise the appropriate exception.
        else:
            raise AppException("Please provide a valid bundle application.")

    except Exception as exc:
        logger.exception(f"Error listing application bundle: {str(exc)}")
        return None


def app_bundle_add(app_name_with_version: str, app_config: Optional[str]) -> bool:
    """

    List all the applications available in an app bundle.

    Parameters
    ----------
    app_name_with_version : The application name with version to add to the application bundle.
    app_config : The app bundle configuration file to process.

    Returns
    -------
    A boolean indicating whether the application was added to the provided bundle.
    """
    try:
        # 1 - Load the bundle App Configuration
        app_config_file_path: KPath = KPath(app_config)
        if not app_config_file_path.exists():
            raise NoApplicationConfigurationProvided()

        # 2 - Retrieve the new application from the platform's registry
        app_to_add = ApplicationName(name=app_name_with_version)
        from kelvin.sdk.lib.common.api.appregistry import appregistry_show

        appregistry_object = appregistry_show(app_name=app_to_add.name, app_version=app_to_add.version)
        kelvin_app_config: dict = {}
        if len(appregistry_object) > 0:
            app_version_object: AppVersion = appregistry_object[0].raw_data
            # 2.1 - Extract its payload
            if app_version_object.payload:
                kelvin_app_config = app_version_object.payload.get("app", {}).get("kelvin", {})

        # 3 - If there is no application configuration, raise an error
        if not kelvin_app_config:
            raise NoApplicationConfigurationProvided()

        # 4 - Parse the application bundle
        bundle_app_configuration = KelvinAppConfiguration(**app_config_file_path.read_yaml())
        if bundle_app_configuration.app.bundle:
            # 4.1 - Get the bundle application name and version and get its 'full' format.
            bundle_app_name_str: str = str(bundle_app_configuration.info.name)
            bundle_app_version_str: str = str(bundle_app_configuration.info.version)
            bundle_app_name = ApplicationName(name=bundle_app_name_str, version=bundle_app_version_str)
            # 4.2 - Create the pipeline entry and add it to the application bundle
            bundle_app_configuration.app.bundle.pipelines.append(
                Pipeline(**{"name": app_to_add.name, "version": app_to_add.version, "kelvin": kelvin_app_config})
            )
            # 4.3 - Commit the changes to the application bundle
            bundle_app_configuration.to_file(path=app_config_file_path, sort_keys=True)
            logger.relevant(f'"{app_to_add.full_name}" successfully added to "{bundle_app_name.full_name}"')
            return True
        # 5 - If it is not an application bundle, raise the appropriate exception.
        else:
            raise AppException("Please provide a valid bundle application.")

    except Exception as exc:
        logger.exception(f"Error adding application to bundle: {str(exc)}")
        return False


def app_bundle_remove(index: int, app_config: Optional[str] = None) -> bool:
    """

    List all the applications available in an app bundle.

    Parameters
    ----------
    index : The application index to remove from the app configuration.
    app_config : The app bundle configuration file to process.

    Returns
    -------
    A boolean indicating whether the application was removed from to the provided bundle.

    """
    try:
        # 1 - Load the bundle App Configuration
        app_config_file_path: KPath = KPath(app_config)
        if not app_config_file_path.exists():
            raise NoApplicationConfigurationProvided()
        bundle_app_configuration = KelvinAppConfiguration(**app_config_file_path.read_yaml())

        # 2 - If there is a bundle (it should), list all of its pipelines
        if bundle_app_configuration.app.bundle:
            # 2.1 - Get the application name and version and get its 'full' format.
            bundle_app_name_str: str = str(bundle_app_configuration.info.name)
            bundle_app_version_str: str = str(bundle_app_configuration.info.version)
            bundle_app_name = ApplicationName(name=bundle_app_name_str, version=bundle_app_version_str)
            # 2.2 - Retrieve the pipelines in the initial state and print each line (if there are any)
            bundle_pipelines = bundle_app_configuration.app.bundle.pipelines
            if bundle_pipelines and index < len(bundle_pipelines):
                # 2.3 - Account for the initial pipelines
                initial_pipelines = [f"{index} - {p.name}:{p.version}" for index, p in enumerate(bundle_pipelines)]
                initial_pipelines_pretty = """\n\t\t\t""".join(initial_pipelines)
                # 2.4
                pipeline_to_delete = bundle_app_configuration.app.bundle.pipelines[index]
                app_name_to_delete_str: str = str(pipeline_to_delete.name)
                app_version_to_delete_str: str = str(pipeline_to_delete.version)
                app_name_to_delete = ApplicationName(name=app_name_to_delete_str, version=app_version_to_delete_str)
                # 2.4 - Delete the targeted index
                del bundle_app_configuration.app.bundle.pipelines[index]
                post_removal_pipelines = bundle_app_configuration.app.bundle.pipelines
                post_pipelines = [f"{index} - {p.name}:{p.version}" for index, p in enumerate(post_removal_pipelines)]
                post_pipelines_pretty = """\n\t\t\t""".join(post_pipelines)
                # 2.5 - Account for the pipelines after index deletion
                complete_message = f"""
                    You are about to remove index {index} (\"{app_name_to_delete.full_name}\") from the bundle:

                    Before:
                    \t{initial_pipelines_pretty}
    
                    After:
                    \t{post_pipelines_pretty}
    
                """
                result = display_yes_or_no_question(question=complete_message)
                if result:
                    bundle_app_configuration.to_file(path=app_config_file_path, sort_keys=True)
                    logger.relevant(f'Application successfully removed from the "{bundle_app_name.full_name}"')
            elif index >= len(bundle_pipelines):
                logger.warning("The provided index does not correspond to any application in the bundle.")
            else:
                logger.warning(f"No application pipelines defined for {bundle_app_name.full_name}")
            return True
        # 3 - If it is not an application bundle, raise the appropriate exception.
        else:
            raise AppException("Please provide a valid bundle application.")

    except Exception as exc:
        logger.exception(f"Error removing application from bundle: {str(exc)}")
        return False


# 2 - internal, utils methods
def _app_create(app_creation_parameters: AppCreationParametersObject) -> bool:
    """
    The entry point for the creation of a App.

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    :param app_creation_parameters: the object containing all the required variables for App creation.

    :return: a bool indicating whether the App creation was successful.

    """
    try:
        logger.info(f'Creating new application "{app_creation_parameters.app_name}"')

        check_if_app_name_is_valid(app_name=app_creation_parameters.app_name)
        try:
            parameters_are_valid = app_creation_parameters.assess_parameters_validity
        except ValueError as exc:
            parameters_are_valid = False
            logger.error(exc)

        if not parameters_are_valid:
            error_message = """The provided parameter combination is not valid.
                Consider creating the application using the wizard:
                Simply type `kelvin app create` and follow the suggested steps.
            """
            raise ValueError(error_message)

        # 2 - Create the base directory and app creation object
        if app_creation_parameters.app_type == AppType.kelvin:
            app_creation_object = get_kelvin_app_creation_object(app_creation_parameters=app_creation_parameters)
        elif app_creation_parameters.app_type == AppType.bundle:
            app_creation_object = get_bundle_app_creation_object(app_creation_parameters=app_creation_parameters)
        else:
            app_creation_object = get_docker_app_creation_object(app_creation_parameters=app_creation_parameters)

        # 3 - Create all required fundamental & optional directories and files
        fundamental_dirs_and_files = app_creation_object.fundamental_dirs_and_files()
        optional_dirs_and_files = app_creation_object.optional_dirs_and_files()

        for dir in fundamental_dirs_and_files + optional_dirs_and_files:
            dir.delete()
            dir.create()
            for file in dir.files:
                file.create()

        app_creation_success: str = f"""Successfully created new application: \"{app_creation_parameters.app_name}\".

        The provided configuration \"app.yaml\" is a base sample.

        You may continue its configuration using \"studio\". Refer to \"kelvin studio --help\" for more information.
        """
        logger.relevant(app_creation_success)

        return True
    except Exception as exc:
        if app_creation_parameters:
            app_name = app_creation_parameters.app_name
            logger.exception(f'Error creating "{app_name}" application: {str(exc)}')
            if app_creation_parameters.app_dir and app_name:
                app_complete_directory = KPath(app_creation_parameters.app_dir) / app_name
                app_complete_directory.delete_dir()

    return False


def _build_docker_app(docker_app_building_object: DockerAppBuildingObject) -> bool:
    """
    The entry point for the building of a 'Docker' type application.

    :param docker_app_building_object: the BaseAppBuildingObject that contains
    all necessary variables to build a docker app.

    :return: a bool indicating whether the Docker application was successfully built.

    """
    docker_manager = get_docker_manager()

    app_name = docker_app_building_object.app_config_model.info.name

    successfully_built = docker_manager.build_docker_app_image(docker_build_object=docker_app_building_object)

    logger.relevant(f'Image successfully built: "{app_name}"')

    return successfully_built


def _build_kelvin_app(kelvin_app_building_object: KelvinAppBuildingObject) -> bool:
    """
    The entry point for the building of a kelvin-type application.

    Package the kelvin application using the either a KelvinAppBuildingObject, thus building a valid docker image.

    :param kelvin_app_building_object: the object that contains all the required variables to build an app.

    :return: a boolean indicating whether the kelvin application was successfully built.

    """
    docker_manager = get_docker_manager()

    app_name = kelvin_app_building_object.full_docker_image_name

    app_build_dir_path = kelvin_app_building_object.app_build_dir_path
    app_config_file_path = kelvin_app_building_object.app_config_file_path
    app_dir_path = kelvin_app_building_object.app_dir_path
    app_build_dir_path.create_dir()

    datamodel_dir_path = setup_datamodels(kelvin_app_building_object=kelvin_app_building_object)
    if datamodel_dir_path is not None:
        kelvin_app_building_object.app_datamodel_dir_path = datamodel_dir_path
        kelvin_app_building_object.build_for_data_model_compilation = bool(datamodel_dir_path)

    logger.debug(f'Provided configuration file path: "{app_config_file_path}"')
    logger.debug(f'Provided application directory: "{app_dir_path}"')

    docker_manager.build_kelvin_app_dockerfile(kelvin_app_building_object=kelvin_app_building_object)
    docker_manager.build_kelvin_app_docker_image(kelvin_app_building_object=kelvin_app_building_object)

    logger.relevant(f'Image successfully built: "{app_name}"')

    kelvin_app = kelvin_app_building_object.app_config_model.app.kelvin
    app_lang = None
    if kelvin_app and kelvin_app.core:
        app_lang = kelvin_app.core.language.type

    return assess_docker_image_version(
        current_docker_image=kelvin_app_building_object.base_image,
        app_lang=ApplicationLanguage(app_lang),
    )


def _build_bundle_app(bundle_app_building_object: BundleAppBuildingObject) -> bool:
    """
    The entry point for the building of a bundle-type application.

    Package the bundle application using the BundleAppBuildingObject, thus building a valid docker image.

    :param bundle_app_building_object: the object that contains all the required variables to build an app.

    :return: a boolean indicating whether the bundle application was successfully built.

    """

    from kelvin.sdk.lib.common.api.appregistry import appregistry_download

    app_name = bundle_app_building_object.full_docker_image_name
    app_build_dir_path = bundle_app_building_object.app_build_dir_path
    app_config_file_path = bundle_app_building_object.app_config_file_path
    app_dir_path = bundle_app_building_object.app_dir_path

    logger.debug(f'Provided configuration file path: "{app_config_file_path}"')
    logger.debug(f'Provided application directory: "{app_dir_path}"')

    bundle_app_object = bundle_app_building_object.app_config_model.app.bundle
    if bundle_app_object is None:
        raise AppException(app_name)

    app_build_dir_path.delete_dir().create_dir()

    bundle_cache = app_build_dir_path / "bundle"
    bundle_cache.create_dir()
    (bundle_cache / "apps").create_dir()
    (bundle_cache / "config").create_dir()

    data_model_cache = app_build_dir_path / "datamodel"
    data_model_cache.create_dir()

    pipelines: List[Pipeline] = bundle_app_object.pipelines
    if not pipelines:
        raise AppException(app_name)

    padding = int(log10(len(pipelines))) + 1

    # collate info over apps
    # system:
    #  - resources (sum, max?)
    #  - privileged (logical-or)
    #  - volumes (combine, look for collisions)
    #  - ports (combine, look for collisions)
    #  - env_vars (combine, look for collisions)

    app_dir = DockerConfigs.app_container_app_dir_path
    bundle_dir = DockerConfigs.app_bundle_dir_path

    system_packages: Set[str] = {*[]}
    data_models: DefaultDict[str, Set[str]] = defaultdict(set)

    try:
        docker_manager = get_docker_manager()

        for i, pipeline in enumerate(pipelines):
            image_name = f"{pipeline.name}:{pipeline.version}"
            pipeline_key = f"pipeline_{i:0{padding}}_{standardize_string(str(pipeline.name))}_{str(pipeline.version).replace('.', '_')}"
            output_dir = bundle_cache / "apps" / pipeline_key

            image_exists = docker_manager.check_if_docker_image_exists(docker_image_name=image_name)
            if not image_exists:
                result = appregistry_download(str(pipeline.name), str(pipeline.version), override_local_tag=True)
                if not result:
                    return False

            # get app
            result = app_images_unpack(image_name, output_dir)
            if not result:
                return False

            app_bundle_build_failure: str = "Error bundling application: {image_name}: {reason}"
            app_config_file = output_dir / GeneralConfigs.default_app_config_file
            try:
                kelvin_app_data = app_config_file.read_yaml()
                if bundle_app_object.core is not None:
                    kelvin_app_data = merge(
                        kelvin_app_data, {"app": {"kelvin": {"core": bundle_app_object.core.dict()}}}
                    )
                if pipeline.kelvin is not None:
                    kelvin_app_data = merge(kelvin_app_data, {"app": {"kelvin": pipeline.kelvin.dict()}})
                if pipeline.configuration is not None:
                    kelvin_app_data = merge(kelvin_app_data, pipeline.configuration)
                kelvin_app_config = KelvinAppConfiguration.parse_obj(kelvin_app_data)
            except Exception as e:
                logger.exception(app_bundle_build_failure.format(image_name=image_name, reason=e))
                return False

            if kelvin_app_config.app.type != AppType.kelvin:
                wrong_app_type: str = app_bundle_build_failure.format(
                    image_name=image_name, reason=f"app type: {kelvin_app_config.app.type.name}"
                )
                logger.error(wrong_app_type)
                return False

            if kelvin_app_config.app.kelvin is None:
                missing_kelvin_app_config: str = app_bundle_build_failure.format(
                    image_name=image_name, reason="missing kelvin app config"
                )
                logger.error(missing_kelvin_app_config)
                return False

            system_packages |= {*(kelvin_app_config.app.kelvin.system_packages or [])}

            core_config = kelvin_app_config.app.kelvin.core

            data_model: DataModel
            for data_model in core_config.data_models:
                data_models[str(data_model.name)] |= {str(data_model.version)}

            for path in (output_dir / "build" / "datamodel").glob("*"):
                (data_model_cache / path.name).write_text(path.read_text())

            # relocate paths
            pipeline_dir = f"{bundle_dir}/apps/{pipeline_key}"

            interface: Interface = core_config.interface
            if interface.type == ApplicationInterface.client:
                if (
                    interface.client is not None
                    and interface.client.executable is not None
                    and not interface.client.executable.startswith("/")
                ):
                    interface.client.executable = f"{pipeline_dir}/{interface.client.executable}"

            language: Language = core_config.language
            if language.type == ApplicationLanguage.cpp:
                if language.cpp is not None:
                    if language.cpp.dso.startswith(f"{app_dir}/"):
                        language.cpp.dso = language.cpp.dso.replace(app_dir, pipeline_dir, 1)

            data = merge(kelvin_app_data, lower(kelvin_app_config.dict()))
            app_config_file.write_yaml(data)
            app_config_file.clone_into(bundle_cache / "config" / f"{pipeline_key}.yaml")

        data_model_dupes = "\n".join(f"  - {k}: {', '.join(sorted(v))}" for k, v in data_models.items() if len(v) > 1)
        if data_model_dupes:
            logger.error(f'Duplicated data models with differing versions:\n"{data_model_dupes}"')
            return False

        bundle_app_building_object.system_packages = [*system_packages]

        docker_manager.build_bundle_app_dockerfile(bundle_app_building_object=bundle_app_building_object)
        docker_manager.build_kelvin_app_docker_image(kelvin_app_building_object=bundle_app_building_object)

    except Exception:
        raise

    return True


def start_data_injector(
    input_file: Sequence[str],
    app_name: Sequence[str],
    endpoint: Optional[str],
    period: float,
    repeat: bool,
    ignore_timestamps: bool,
) -> bool:
    """
    Start the embedded Injector app that will inject data into the emulation system..

    :param input_file: the sequence of files that will be injected into the system.
    :param app_name: the app into which the data will be injected.
    :param endpoint: the endpoint to publish data into.
    :param period: the rate at which data will be polled from the application.
    :param repeat: indicates whether the injection should repeat forever.
    :param ignore_timestamps: ignore timestamps in data.

    :return: a boolean indicating whether the injector was successfully started.

    """

    filenames = [KPath(x).resolve() for x in input_file]
    root = min(x.parent for x in filenames)

    return build_data_app(
        "injector",
        "kelvin.sdk.injector:InjectorApp",
        app_name,
        routing={"inputs": "outputs"},
        endpoint=endpoint,
        period=period,
        data_files=filenames,
        configuration=[
            IO(
                name="injector",
                data_model="kelvin.sdk.injector.config",
                values=[
                    Item(name="filenames", value=[f"data/{x.relative_to(root)}" for x in filenames]),
                    Item(name="repeat", value=repeat),
                    Item(name="ignore_timestamps", value=ignore_timestamps),
                ],
            )
        ],
    )


def start_data_extractor(app_name: Sequence[str], shared_dir: str, batch: float) -> bool:
    """
    Start the embedded Extractor app that will extract data from the emulation system..

    :param app_name: the sequence of apps to extract data from.
    :param shared_dir: the directory shared between the container and the host machine.
    :param batch: the extractor batch write frequency.

    :return: a boolean indicating whether the extractor was successfully started.

    """

    output_path = f"{DockerConfigs.app_container_shared_dir_path}/output"

    return build_data_app(
        "extractor",
        "kelvin.sdk.extractor:ExtractorApp",
        app_name,
        routing={"outputs": "inputs"},
        configuration=[
            IO(
                name="extractor",
                data_model="kelvin.sdk.extractor.config",
                values=[
                    Item(name="batch", value=batch),
                    Item(name="output_path", value=output_path),
                ],
            ),
        ],
        shared_dir=shared_dir,
    )


def build_data_app(
    app_name: str,
    entry_point: str,
    image_names: Sequence[str],
    routing: Mapping[IOType, IOType],
    endpoint: Optional[str] = None,
    period: float = 1.0,
    data_files: Optional[Sequence[KPath]] = None,
    configuration: Optional[List[IO]] = None,
    parameters: Optional[List[IO]] = None,
    shared_dir: Optional[str] = None,
) -> bool:
    """Build data app (e.g. injector/extractor)"""

    from kelvin.sdk.lib.common.api.appregistry import appregistry_download

    app_data_failure: str = "Error building data application: {image_name}: {reason}"

    app_dir = DockerConfigs.app_container_app_dir_path
    app_config_filename = GeneralConfigs.default_app_config_file

    image_app_config_filename = f"{app_dir}/{app_config_filename}"
    image_data_model_dir = f"{app_dir}/{GeneralConfigs.default_datamodel_dir}"

    registry_maps: DefaultDict[str, RegistryMap] = defaultdict(RegistryMap)
    data_models: List[DataModel] = []
    data_model_versions: DefaultDict[str, Set[str]] = defaultdict(set)
    io: DefaultDict[str, List[IO]] = defaultdict(list)

    try:
        docker_manager = get_docker_manager()

        with TemporaryDirectory(dir=OSInfo.temp_dir) as temp_dir:
            cache_dir = KPath(temp_dir)
            data_model_dir = cache_dir / GeneralConfigs.default_datamodel_dir
            data_model_dir.mkdir()

            # extract inputs across target apps
            for image_name in image_names:
                image_exists = docker_manager.check_if_docker_image_exists(docker_image_name=image_name)
                if not image_exists:
                    if ":" not in image_name:
                        logger.error(f'App name must include version: "{image_name}"')
                        return False
                    name, version = image_name.rsplit(":", 1)
                    result = appregistry_download(name, version, override_local_tag=True)
                    if not result:
                        return False

                # get app config
                result = app_images_unpack(image_name, str(cache_dir), image_dir=image_app_config_filename)
                if not result:
                    return False

                # get data models
                result = app_images_unpack(image_name, str(cache_dir), image_dir=image_data_model_dir, clean_dir=False)
                if not result:
                    return False

                app_config_file = cache_dir / app_config_filename
                try:
                    kelvin_app_config: KelvinAppConfiguration = KelvinAppConfiguration.parse_obj(
                        app_config_file.read_yaml()
                    )
                except Exception as e:
                    logger.exception(app_data_failure.format(image_name=image_name, reason=e))
                    return False

                if kelvin_app_config.app.type != AppType.kelvin:
                    wrong_app_type: str = app_data_failure.format(
                        image_name=image_name, reason=f"app type: {kelvin_app_config.app.type.name}"
                    )
                    logger.error(wrong_app_type)
                    return False

                if kelvin_app_config.app.kelvin is None:
                    missing_kelvin_app_config: str = app_data_failure.format(
                        image_name=image_name, reason="missing kelvin app config"
                    )
                    logger.error(missing_kelvin_app_config)
                    return False

                core_config: Core = kelvin_app_config.app.kelvin.core

                data_model: DataModel
                for data_model in core_config.data_models:
                    versions = data_model_versions[str(data_model.name)]
                    n = len(versions)
                    versions |= {str(data_model.version)}
                    if len(versions) > n:
                        data_models += [data_model]

                connections = [
                    x.opcua for x in core_config.connections if x.type == ConnectionType.opcua and x.opcua is not None
                ]
                if endpoint is not None:
                    helper_endpoint = OPCUAEndpoint(__root__=endpoint)
                    connections = [x for x in connections if x.endpoint == helper_endpoint]

                if not connections:
                    logger.warning(f'App has no connections: "{image_name}"')
                    continue

                for source, target in routing.items():
                    items = getattr(core_config, source, None)
                    if items is None:
                        continue
                    io[target] += items
                    for connection in connections:
                        items = getattr(connection.registry_map, source)
                        if not items:
                            continue
                        registry_map = registry_maps[str(connection.endpoint)]
                        dest = getattr(registry_map, target)
                        dest += items

            data_model_dupes = "\n".join(
                f"  - {k}: {', '.join(sorted(v))}" for k, v in data_model_versions.items() if len(v) > 1
            )
            if data_model_dupes:
                logger.error(f'Duplicated data models with differing versions:\n"{data_model_dupes}"')
                return False

            if endpoint is not None:
                url = endpoint
            else:
                endpoints = [*registry_maps]
                if len(endpoints) != 1:
                    str_endpoints = ", ".join(endpoints)
                    logger.error(f'App has more than one endpoint: "{str_endpoints}"')
                    return False
                url = endpoints[0]

            hostname = urlparse(url).hostname

            info = Info(name=app_name, title=app_name, description=app_name, version="0.0.0")
            app_config = KelvinAppConfiguration(
                spec_version="1.0.0",
                info=info,
                app=App(
                    type=AppType.kelvin,
                    kelvin=KelvinAppType(
                        images=Images(base="", builder=""),
                        system_packages=[],
                        core=Core(
                            version="4.0.0",
                            data_models=data_models,
                            connections=[
                                Connection(
                                    name=f"connection-{i}",
                                    type=ConnectionType.opcua,
                                    opcua=OPCUAConnectionType(registry_map=registry_map, endpoint=endpoint),
                                )
                                for i, (endpoint, registry_map) in enumerate(registry_maps.items())
                            ],
                            interface=Interface(
                                type=ApplicationInterface.client,
                                client=ClientInterfaceType(
                                    period=period,
                                    executable=f"{app_dir}/venv/bin/python",
                                    args=[
                                        "-m",
                                        "kelvin.app",
                                        "run",
                                        "app",
                                        "-c",
                                        image_app_config_filename,
                                        entry_point,
                                    ],
                                    spawn=True,
                                ),
                            ),
                            language=Language(
                                type=ApplicationLanguage.python,
                                python=PythonLanguageType(
                                    entry_point=entry_point,
                                    requirements=str(cache_dir / "requirements.txt"),
                                ),
                            ),
                            **io,
                        ),
                    ),
                ),
            )
            if configuration is not None:
                if app_config.app.kelvin:
                    app_config.app.kelvin.core.configuration += configuration
            if parameters is not None:
                if app_config.app.kelvin:
                    app_config.app.kelvin.core.parameters += parameters

            (cache_dir / app_config_filename).write_yaml(lower(app_config.dict(exclude_none=True)))
            (cache_dir / "requirements.txt").write_text("kelvin-app[data]")
            if data_files is not None:
                (cache_dir / "data").mkdir()
                root = min(x.parent for x in data_files)
                for x in data_files:
                    x.clone_into(cache_dir / "data" / x.relative_to(root))

            with chdir(cache_dir):
                result = app_build(temp_dir)
                if not result:
                    return False

            return emulation_start(
                app_name, net_alias=hostname, shared_dir_path=shared_dir, show_logs=True, is_external_app=True
            )

    except Exception as exc:
        str_image_names = ", ".join(image_names)
        logger.exception(f"Error building data application: {str_image_names}: {str(exc)}")
        return False
