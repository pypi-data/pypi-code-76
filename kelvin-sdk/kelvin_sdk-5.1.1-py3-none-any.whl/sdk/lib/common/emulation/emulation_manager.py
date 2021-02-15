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

from typing import Dict, List, Optional

from kelvin.sdk.lib.common.configs.internal.docker_configs import DockerConfigs
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.docker.docker_manager import DockerManager
from kelvin.sdk.lib.common.exceptions import EmulationException
from kelvin.sdk.lib.common.models.factories.app_setup_configuration_objects_factory import get_default_app_name
from kelvin.sdk.lib.common.models.factories.docker_manager_factory import get_docker_manager
from kelvin.sdk.lib.common.models.generic import GenericObject, KPath
from kelvin.sdk.lib.common.models.ksdk_docker import AppRunningContainers, DockerContainer, DockerImage
from kelvin.sdk.lib.common.schema.schema_manager import validate_app_schema_from_app_config_file
from kelvin.sdk.lib.common.utils.display_utils import display_data_entries
from kelvin.sdk.lib.common.utils.logger_utils import logger


def emulation_start(
    app_name: Optional[str] = None,
    app_config_path: Optional[str] = None,
    port_mapping: Optional[List[str]] = None,
    volumes: Optional[List[str]] = None,
    arguments: Optional[List[str]] = None,
    environment_variables: Optional[Dict] = None,
    shared_dir_path: Optional[str] = None,
    net_alias: Optional[str] = None,
    entrypoint: Optional[str] = None,
    attach: bool = False,
    show_logs: bool = False,
    is_external_app: bool = False,
) -> bool:
    """
    Start an application on the emulation system.

    :param app_name: the application's name.
    :param app_config_path: the application configuration file to be used on the emulation.
    :param port_mapping: the port to be mapped between the container and the host machine.
    :param volumes: the volumes to be mapped between container and host machine.
    :param arguments: additional arguments to be passed on to the docker image.
    :param environment_variables: additional environment variables to be passed on to the docker image.
    :param shared_dir_path: the path to the desired shared dir.
    :param net_alias: the network alias.
    :param entrypoint: override the entrypoint of the application.
    :param attach: attach to container.
    :param show_logs: if provided, will start displaying longs once the app is emulated.
    :param is_external_app: indicates whether or not the application is external.

    :return: a boolean indicating whether the App was successfully started.

    """
    try:
        app_name = app_name or get_default_app_name()

        # 1 - Retrieve the docker manager
        docker_manager = get_docker_manager()

        # 2 - Start the network
        _start_ksdk_network(docker_manager=docker_manager)

        logger.info("Loading configuration and starting the application")

        # 3 - Check if the app exists
        application_exists = docker_manager.check_if_docker_image_exists(
            docker_image_name=app_name, all_images=is_external_app
        )

        if not application_exists:
            raise EmulationException(f'\tProvided application "{app_name}" not found\n')

        logger.info(f'Starting application "{app_name}"')

        # 4 - Setup up the shared directory binding
        volume_bindings = _get_volume_bindings(volumes=volumes, shared_dir_path=shared_dir_path)

        # 5 - Prepare the host config and port mapping
        port_mapping_dict = _get_port_mapping(port_mapping=port_mapping)
        host_config = docker_manager.get_container_host_config(
            binds=volume_bindings, port_mapping=port_mapping_dict, auto_remove=False
        )

        # 6 - If an app configuration is provided, its schema mus be validated.
        if app_config_path:
            validate_app_schema_from_app_config_file(app_config_file_path=KPath(app_config_path))

        # 7 - Run the image with the host config
        image_was_ran = docker_manager.run_app_docker_image(
            docker_image_name=app_name,
            host_config=host_config,
            app_config_path=app_config_path,
            net_alias=net_alias,
            entrypoint=entrypoint,
            attach=attach,
            arguments=arguments,
            environment_variables=environment_variables,
        )

        if not image_was_ran:
            raise EmulationException(f'Error starting pre-built application "{app_name}"')

        if show_logs:
            image_was_ran = emulation_logs(app_name=app_name)
            return image_was_ran

        if image_was_ran:
            logger.relevant(f'Application successfully launched: "{app_name}"')

        return True

    except Exception as exc:
        logger.exception(f"Error emulating application:\n{str(exc)}")
        return False


def emulation_stop(app_name: Optional[str], should_stop_network: bool = True) -> bool:
    """
    Stop a running application.

    :param app_name: the name of the app to stop.
    :param should_stop_network: indicates whether the ksdk network should also be stopped.

    :return: a boolean indicating whether the App was successfully stopped.

    """
    try:
        app_name = app_name or get_default_app_name()

        logger.info(f'Attempting to stop application "{app_name}"')

        docker_manager = get_docker_manager()

        app_was_stopped = docker_manager.stop_docker_containers_for_image(docker_image_name=app_name)

        if app_was_stopped:
            logger.relevant("Application was successfully stopped")
        else:
            logger.warning("No running instances of the provided application were found")

        if should_stop_network:
            images_and_containers = get_all_app_images_and_running_containers(should_display=False)
            if not images_and_containers.existing_containers:
                _stop_ksdk_network(docker_manager=docker_manager)

        return True

    except Exception as exc:
        logger.exception(f"Error stopping application: {str(exc)}")
        return False


def emulation_logs(app_name: Optional[str], tail: bool = False) -> bool:
    """
    Display the logs of a running application.

    :param app_name: the name of the application to retrieve the logs from.
    :param tail: indicates whether it should tail the logs and return.

    :return: a symbolic flag indicating the logs were successfully obtained.

    """
    try:
        app_name = app_name or get_default_app_name()

        docker_manager = get_docker_manager()

        successful_logs = docker_manager.get_logs_for_docker_container(docker_image_name=app_name, tail=tail)

        if not successful_logs:
            raise EmulationException(message="Provided application not found")

        return successful_logs

    except Exception as exc:
        logger.exception(f"Error retrieving logs for the provided application: {str(exc)}")
        return False


def get_all_app_images_and_running_containers(should_display: bool = False) -> AppRunningContainers:
    """
    Retrieve the current status of the application images as well as the current running processes.

    Will yield 2 tables: the first containing the existing Apps and the second containing all the running
    processes.

    :param should_display: specifies whether or not the display should output data.

    :return: a tuple containing both App images and App running containers.

    """
    try:
        ksdk_labels = DockerConfigs.ksdk_app_identification_label

        docker_manager = get_docker_manager()
        existing_ksdk_images: List[DockerImage] = docker_manager.get_docker_images(labels=ksdk_labels)
        existing_ksdk_containers: List[DockerContainer] = docker_manager.get_docker_containers(labels=ksdk_labels)
        running_ksdk_containers = [container for container in existing_ksdk_containers if container.running]

        filtered_ksdk_images = [
            GenericObject(data={"tag": tag, "readable_created_date": image.readable_created_date})
            for image in existing_ksdk_images
            if any("<none>" not in tag for tag in image.tags)
            for tag in image.tags
        ]

        if should_display:
            display_data_entries(
                data=filtered_ksdk_images,
                header_names=["Applications", "Created"],
                attributes=["tag", "readable_created_date"],
                table_title=GeneralConfigs.table_title.format(title="Existing Apps"),
                no_data_message="No application available on the local registry",
            )
            display_data_entries(
                data=running_ksdk_containers,
                header_names=[
                    "Running applications",
                    "Containers",
                    "Up and running",
                    "Local IP Address",
                    "Ports (container->host)",
                ],
                attributes=["image_name", "container_names", "running", "id_address", "ports"],
                table_title=GeneralConfigs.table_title.format(title="Running Apps"),
                no_data_message="No applications running",
            )

        return AppRunningContainers(existing_images=existing_ksdk_images, existing_containers=existing_ksdk_containers)

    except Exception as exc:
        logger.exception(f"Error retrieving application information: {str(exc)}")
        return AppRunningContainers()


# Utils
def _get_port_mapping(port_mapping: Optional[List[str]]) -> dict:
    """
    When provided with a port mapping string (of the port:port format), yield a dictionary

    :param port_mapping: the string of the port mapping. E.g. 48010:48010

    :return: a dictionary that maps host port to container port
    """
    if port_mapping:
        result: Dict[str, str] = {}
        for port in port_mapping:
            container_port, host_port = port.split(":", 1)
            logger.debug(f'Connecting container port "{container_port}" to host port "{host_port}"')
            result[container_port] = host_port
        return result
    else:
        return {}


def _get_volume_bindings(volumes: Optional[List[str]], shared_dir_path: Optional[str]) -> List[str]:
    """
    Yield the volume string that maps host volume to container volume.
    Additionally, and if specified, will map the storage of the container to the host machine for raw database access.

    :param volumes: the path to the shared directory.
    :param shared_dir_path: the path to the shared directory.

    :return: a List of strings containing the volumes.

    """
    volume_bindings = volumes or []

    # 1 - Prepare the shared container volume binding
    if shared_dir_path:
        shared_dir_path = KPath(shared_dir_path).absolute()
        shared_container_dir = DockerConfigs.app_container_shared_dir_path
        shared_data_bind = DockerConfigs.app_container_shared_dir_bind
        shared_data_bind = shared_data_bind.format(shared_dir_path=shared_dir_path)
        volume_bindings.append(shared_data_bind)

        start_app_shared_folder_info: str = f"""

            Shared volume established.

            The following will be linked (host -> container): \"{shared_dir_path}\" <-> \"{shared_container_dir}\"

            All data output to \"{shared_container_dir}\" will be available in \"{shared_dir_path}\".
        """
        logger.relevant(start_app_shared_folder_info)

    return volume_bindings


# Network
def _start_ksdk_network(docker_manager: DockerManager) -> bool:
    """
    Start the KSDK network of the provided DockerManager.

    :param docker_manager: the object that encapsulates the docker utility instance.

    :return: a boolean indicating whether the ksdk network was successfully started.

    """
    try:
        logger.info("Initializing the emulation system.")

        network_already_running = _is_ksdk_network_online(docker_manager=docker_manager)

        if network_already_running:
            return True

        # Launch the network, building the bus app and launch it
        network_successfully_started = docker_manager.create_docker_network()

        logger.relevant("Emulation system successfully started")

        return network_successfully_started

    except Exception as exc:
        logger.exception(f"Error starting the emulation system: {str(exc)}")
        return False


def _stop_ksdk_network(docker_manager: DockerManager) -> bool:
    """
    Stop the KSDK network of the provided DockerManager.

    :param docker_manager: the object that encapsulates the docker utility instance.

    :return: a boolean indicating whether the ksdk network was successfully stopped.

    """
    try:
        logger.info("Stopping the emulation system.")

        # Remove the 'ksdk' docker network
        docker_manager.remove_docker_network()
        # Remove "dangling" containers
        docker_manager.prune_docker_containers()
        # Remove "dangling" images
        docker_manager.prune_docker_images()

        logger.relevant("Emulation system successfully stopped")

        return True

    except Exception as exc:
        logger.exception(f"Error stopping the emulation system: {str(exc)}")
        return False


def _is_ksdk_network_online(docker_manager: DockerManager) -> bool:
    """
    Verifies the current status of the provided network.

    :param docker_manager: the object that encapsulates the docker utility instance.

    :return: a boolean indicating whether the ksdk network is currently online.

    """
    try:
        network_id = docker_manager.get_docker_network_id()
        ksdk_network_is_online = bool(network_id)

        message = "Emulation system is running." if ksdk_network_is_online else "Emulation system is not running."
        logger.info(message)

        return ksdk_network_is_online

    except Exception as exc:
        logger.exception(f"Error retrieving emulation system status: {str(exc)}")
        return False
