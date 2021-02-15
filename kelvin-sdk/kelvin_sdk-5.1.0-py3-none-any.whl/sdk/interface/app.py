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

from typing import List, Optional, Tuple

from typeguard import typechecked

from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationLanguage
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import AppType


def app_create_from_wizard() -> bool:
    """
    The entry point for the creation of an application. (WizardTree)

    Usually initiated when no parameters are provided.

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    :return: a bool indicating whether the App creation was successful.

    """
    from kelvin.sdk.lib.common.apps.local_apps_manager import app_create_from_wizard as _app_create_from_wizard

    return _app_create_from_wizard()


@typechecked
def app_create_from_parameters(
    app_dir: str,
    app_name: str,
    app_description: Optional[str],
    app_type: Optional[AppType],
    kelvin_app_lang: Optional[ApplicationLanguage],
) -> bool:
    """
    The entry point for the creation of an application. (Parameters)

    - Creates the directory that will contain the app app.
    - Creates all necessary base files for the development of the app.

    :param app_dir: the app's targeted dir. Will contain all the application files.
    :param app_name: the name of the new app.
    :param app_description: the description of the new app.
    :param app_type: the type of the new application. # E.g. 'docker', 'kelvin'.
    :param kelvin_app_lang: the language the new app will be written on. For kelvin apps only. # E.g. python.

    :return: a bool indicating whether the App creation was successful.

    """

    from kelvin.sdk.lib.common.apps.local_apps_manager import app_create_from_parameters as _app_create_from_parameters

    return _app_create_from_parameters(
        app_dir=app_dir,
        app_name=app_name,
        app_description=app_description,
        app_type=app_type,
        kelvin_app_lang=kelvin_app_lang,
    )


@typechecked
def app_build(app_dir: str, fresh_build: bool = False) -> bool:
    """
    The entry point for the building of a App.

    Package the App on the provided app directory.

    :param app_dir: the path where the application is hosted.
    :param fresh_build: If specified will remove any cache and rebuild the application from scratch.

    :return: a boolean indicating whether the App was successfully built.

    """
    from kelvin.sdk.lib.common.apps.local_apps_manager import app_build as _app_build

    return _app_build(app_dir=app_dir, fresh_build=fresh_build)


@typechecked
def app_migrate(app_dir: str) -> bool:
    """
    Migrate the application configuration to the new schema version.

    :param app_dir: the path to the application that requires migrate.

    :return: a boolean indicating whether the App was successfully migrate.

    """
    from kelvin.sdk.lib.common.apps.local_apps_manager import app_migrate as _app_migrate

    return _app_migrate(app_dir_path=app_dir)


def app_images_list() -> Tuple[List, List]:
    """
    Retrieve the current status of the application images as well as the current running processes.

    Will yield 2 tables: the first containing the existing Apps and the second containing all the running
    processes.

    :return: a tuple containing both App images and App running containers.

    """
    from kelvin.sdk.lib.common.emulation.emulation_manager import get_all_app_images_and_running_containers

    all_app_images_and_containers = get_all_app_images_and_running_containers(should_display=True)

    return all_app_images_and_containers.existing_images, all_app_images_and_containers.existing_containers


@typechecked
def app_images_remove(app_name_with_version: str) -> bool:
    """
    Remove the specified application from the existing image list (in the docker instance).

    :param app_name_with_version: the app to be removed. Must include the version.

    :return: a boolean indicating whether the application was successfully removed.

    """
    from kelvin.sdk.lib.common.apps.local_apps_manager import app_images_remove as _app_images_remove

    return _app_images_remove(app_name_with_version=app_name_with_version)


@typechecked
def app_images_unpack(app_name_with_version: str, output_dir: str) -> bool:
    """
    Extract the content of an application from its built image.

    :param app_name_with_version: the name of the image to unpack the app from.
    :param output_dir: the output directory to output the application content.

    :return: a boolean indicating whether the application was successfully unpacked and extracted.

    """
    from kelvin.sdk.lib.common.apps.local_apps_manager import app_images_unpack as _app_images_unpack

    return _app_images_unpack(app_name_with_version=app_name_with_version, output_dir=output_dir)


@typechecked()
def app_bundle_list(app_config: str) -> Optional[List[str]]:
    """

    List all the applications available in an app bundle.

    Parameters
    ----------
    app_config : The app bundle configuration file to process.

    Returns
    -------
    A list of strings containing both app name and version.
    """
    from kelvin.sdk.lib.common.apps.local_apps_manager import app_bundle_list as _app_bundle_list

    return _app_bundle_list(app_config=app_config)


@typechecked()
def app_bundle_add(app_name_with_version: str, app_config: str) -> bool:
    """

    Add an application to an existing bundle.

    Parameters
    ----------
    app_name_with_version : The application name with version to add to the application bundle.
    app_config : The app bundle configuration file to process.

    Returns
    -------
    A boolean indicating whether the application was added to the provided bundle.
    """
    from kelvin.sdk.lib.common.apps.local_apps_manager import app_bundle_add as _app_bundle_add

    return _app_bundle_add(app_name_with_version=app_name_with_version, app_config=app_config)


@typechecked()
def app_bundle_remove(index: int, app_config: str) -> bool:
    """
    Remove an application from an existing bundle.

    Parameters
    ----------
    index : The application index to remove from the app configuration.
    app_config : The app bundle configuration file to process.

    Returns
    -------
    A boolean indicating whether the application was removed from to the provided bundle.

    """
    from kelvin.sdk.lib.common.apps.local_apps_manager import app_bundle_remove as _app_bundle_remove

    return _app_bundle_remove(index=index, app_config=app_config)
