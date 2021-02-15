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

from typing import Any, List, Optional, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import AppCreate
from kelvin.sdk.lib.common.api.workload import retrieve_workload_and_workload_status_data
from kelvin.sdk.lib.common.apps.local_apps_manager import app_build
from kelvin.sdk.lib.common.auth.auth_manager import (
    login_client_on_current_url,
    retrieve_error_message_from_api_exception,
)
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.exceptions import AppException
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.common.models.apps.ksdk_app_setup import ApplicationName
from kelvin.sdk.lib.common.models.factories.app_setup_configuration_objects_factory import get_default_app_configuration
from kelvin.sdk.lib.common.models.factories.docker_manager_factory import get_docker_manager
from kelvin.sdk.lib.common.models.factories.global_configurations_objects_factory import (
    get_docker_credentials_for_current_url,
)
from kelvin.sdk.lib.common.models.generic import KPath
from kelvin.sdk.lib.common.utils.display_utils import (
    DisplayObject,
    display_data_entries,
    display_data_object,
    display_yes_or_no_question,
)
from kelvin.sdk.lib.common.utils.logger_utils import logger


def appregistry_list(query: Optional[str] = None, should_display: bool = False) -> List[DisplayObject]:
    """
    Returns the list of apps on the registry.

    :param query: the query to search for.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the applications available on the platform.

    """
    try:
        appregistry_list_step_1 = "Retrieving apps.."
        if query:
            appregistry_list_step_1 = f'Searching applications that match "{query}"'

        logger.info(appregistry_list_step_1)

        display_obj = retrieve_appregistry_data(query=query, should_display=should_display)

        return [display_obj]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error listing apps: {error_message}")

    except Exception as exc:
        logger.exception(f"Error listing apps: {str(exc)}")

    return []


def appregistry_show(app_name: str, app_version: Optional[str], should_display: bool = False) -> List[DisplayObject]:
    """
    Returns detailed information on the specified application.

    :param app_name: the name of the app.
    :param app_version: the version to consult.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the yielded Appregistry application instance and its data.

    """
    try:
        application_name = ApplicationName(name=app_name, version=app_version)

        app_data: Any
        app_version_display = None
        app_info_table_title: str = GeneralConfigs.table_title.format(title="App info")

        if application_name.version:
            params = application_name.dict()
            logger.info('Retrieving details for version "{version}" of "{name}"'.format_map(params))
            client = login_client_on_current_url()
            app_data = client.app.get_app_version(app_name=application_name.name, app_version=application_name.version)
            app_data_display_object = display_data_object(
                data=app_data, should_display=False, object_title=app_info_table_title
            )
            data_to_display = app_data_display_object.tabulated_data
        else:
            logger.info(f'Retrieving details for "{application_name.name}"')
            client = login_client_on_current_url()
            app_data = client.app.get_app(app_name=application_name.name)
            app_data_without_version = app_data.copy(exclude={"versions"})
            app_data_display_object = display_data_object(
                data=app_data_without_version, should_display=False, object_title=app_info_table_title
            )
            data_to_display = app_data_display_object.tabulated_data

            # Display App Versions
            if app_data and app_data.versions:
                app_version_display_object = display_data_entries(
                    data=app_data.versions,
                    header_names=["Version", "Updated"],
                    attributes=["version", "updated"],
                    table_title=GeneralConfigs.table_title.format(title="App Versions"),
                    should_display=False,
                )
                data_to_display += "\n" + app_version_display_object.tabulated_data

        # Retrieve workload data for display
        logger.info(f'Retrieving workloads for "{application_name.name}"')
        workload_display = retrieve_workload_and_workload_status_data(
            app_name=application_name.name, app_version=application_name.version, should_display=False
        )
        if should_display:
            logger.info(f"{data_to_display}\n{workload_display.tabulated_data}")

        return [x for x in [app_data_display_object, app_version_display, workload_display] if x]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error showing app: {error_message}")

    except Exception as exc:
        logger.exception(f"Error showing app: {str(exc)}")

    return []


def appregistry_delete(app_name: str, app_version: Optional[str], ignore_destructive_warning: bool = False) -> bool:
    """
    Deletes the specified application the platform's app registry.

    :param app_name: the name of the app to be deleted.
    :param app_version: the version to delete.
    :param ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    :return: a boolean indicating the end of the app deletion operation.

    """
    try:
        application_name = ApplicationName(name=app_name, version=app_version)

        if application_name.version:
            if not ignore_destructive_warning:
                delete_app_version_prompt: str = """
                    This operation will delete version \"{version}\" of the application \"{name}\".
                    This will also delete ALL workloads and local data associated with this version of the application.
                    
                """.format_map(
                    application_name.dict()
                )
                ignore_destructive_warning = display_yes_or_no_question(delete_app_version_prompt)
            if ignore_destructive_warning:
                params = application_name.dict()
                logger.info('Deleting version "{version}" of the application "{name}"'.format_map(params))
                client = login_client_on_current_url()
                client.app.delete_app_version(app_name=application_name.name, app_version=app_version)
                params = application_name.dict()
                logger.relevant('Version "{version}" of "{name}" successfully deleted.'.format_map(params))
        else:
            if not ignore_destructive_warning:
                appregistry_delete_all_confirmation: str = f"""
                    This operation will delete ALL versions of the application \"{application_name.name}\".
                    This will also delete ALL workloads associated with this application.
                    
                """
                ignore_destructive_warning = display_yes_or_no_question(appregistry_delete_all_confirmation)
            if ignore_destructive_warning:
                logger.info(f'Deleting application: "{application_name.name}"')
                client = login_client_on_current_url()
                client.app.delete_app(app_name=application_name.name)
                logger.relevant(f'Application successfully deleted: "{application_name.name}"')

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error deleting application: {error_message}")

    except Exception as exc:
        logger.exception(f"Error deleting application: {str(exc)}")

    return False


def appregistry_upload(app_dir_path: str, upload_datamodels: bool = False) -> bool:
    """
    Uploads the specified application to the platform.

    - Packages the app
    - Pushes the app to the docker registry
    - Publishes the app on the appregistry endpoint.

    :param app_dir_path: the path to the applications dir.
    :param upload_datamodels: If specified, will upload locally defined datamodels.

    :return: a boolean indicating whether the upload operation was successful.

    """
    try:
        logger.info(f'Uploading application from path: "{KPath(app_dir_path).absolute()}"')

        # 1 - Get all the necessary credentials registry credentials
        user_credentials = get_docker_credentials_for_current_url()
        docker_registry_url = user_credentials.full_registry_url

        # 2 - Load App-level configurations
        default_app_yaml = GeneralConfigs.default_app_config_file
        app_config_file_path: KPath = KPath(app_dir_path) / default_app_yaml
        app_config: KelvinAppConfiguration = get_default_app_configuration(app_config_file_path=app_config_file_path)

        docker_image_name = app_config.info.app_name_with_version
        app_name: str = str(app_config.info.name)
        app_version: str = str(app_config.info.version)
        client = login_client_on_current_url()

        # 3 - Check if the application already exists
        app_version_already_exists = True
        try:
            client.app.get_app_version(app_name=app_name, app_version=app_version)
        except APIError as exc:
            for error in exc.errors:
                if error.http_status_code == 404:
                    app_version_already_exists = False
                    break
        if app_version_already_exists:
            raise AppException(message="The application version you're providing already exists")

        # 4 - Build the application
        app_successfully_packaged = app_build(
            app_dir=app_dir_path, build_for_upload=True, upload_datamodels=upload_datamodels
        )
        if not app_successfully_packaged:
            raise AppException("Error building application during upload phase")

        # 5 - Push the application to the appregistry
        docker_manager = get_docker_manager()
        logger.info(f'Pushing application content to "{docker_registry_url}"')
        push_was_successful = docker_manager.push_docker_image_to_registry(docker_image_name=docker_image_name)
        if not push_was_successful:
            raise AppException(f'Error pushing application "{docker_image_name}" to "{docker_registry_url}"')
        logger.relevant(f'Application "{docker_image_name}" successfully pushed to registry "{docker_registry_url}"')

        # 6 - Create the application on the app endpoint
        app_create_request: AppCreate = AppCreate(payload=app_config_file_path.read_yaml())
        newly_created_app = client.app.create_app(data=app_create_request)
        if newly_created_app:
            appregistry_upload_success: str = f"""\n
                Application successfully uploaded:
                    Name: {app_name}
                    Version: {app_version}

                To deploy this application version, run the following command:
                        kelvin workload deploy --app-name {app_name} --app-version {app_version}
            """
            logger.relevant(appregistry_upload_success)

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error uploading application: {error_message}")

    except Exception as exc:
        logger.exception(f"Error uploading application: {str(exc)}")

    return False


def appregistry_download(app_name: str, app_version: str, override_local_tag: bool = False) -> bool:
    """
    Downloads the specified application from the platform's app registry.

    :param app_name: the name of the app to be downloaded.
    :param app_version: the version corresponding to the app.
    :param override_local_tag: specifies whether or not it should override the local tag.

    :return: a boolean indicating whether the app download operation was successful.

    """
    try:
        application_name = ApplicationName(name=app_name, version=app_version)

        logger.info(f'Downloading application "{application_name.full_name}"')

        docker_manager = get_docker_manager()
        docker_manager.login_on_docker_registry()

        image_pulled = docker_manager.pull_docker_image_from_registry(
            docker_image_name=application_name.full_name, override_local_tag=override_local_tag
        )

        if image_pulled:
            logger.relevant(f'Application "{application_name.full_name}" successfully downloaded to the local registry')
            logger.relevant("Use `kelvin app images unpack` to extract its contents.")

        return True

    except Exception as exc:
        logger.exception(f"Error downloading application: {str(exc)}")

    return False


def retrieve_appregistry_data(query: Optional[str] = None, should_display: bool = True) -> DisplayObject:
    """
    Centralize the call to list apps.
    Retrieve all apps that match the provided criteria and yield the result.

    :param query: the query to search specific apps.
    :param should_display: if specified, will display the results of this retrieve operation.

    :return: a DisplayObject containing the apps.

    """
    client = login_client_on_current_url()

    yielded_apps = cast(List, client.app.list_apps(search=query)) or []

    return display_data_entries(
        data=yielded_apps,
        header_names=["Name", "Title", "Type", "Latest Version", "Updated"],
        attributes=["name", "title", "type", "latest_version", "updated"],
        table_title=GeneralConfigs.table_title.format(title="Apps"),
        should_display=should_display,
        no_data_message="No Apps available",
    )
