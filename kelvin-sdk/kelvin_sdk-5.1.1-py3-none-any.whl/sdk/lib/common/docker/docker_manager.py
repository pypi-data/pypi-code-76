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
import tarfile
from pathlib import Path, PurePosixPath
from random import randint
from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Optional

from docker import APIClient  # type: ignore
from docker.errors import APIError, DockerException, NotFound
from docker.types import HostConfig
from jinja2 import Template

from kelvin.sdk.lib.common.configs.internal.docker_configs import DockerConfigs
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs, GeneralMessages
from kelvin.sdk.lib.common.docker.docker_utils import (
    assess_docker_connection_exception,
    display_docker_progress,
    ensure_docker_is_running,
    handle_error_stack_trace,
    process_dockerfile_build_entry,
)
from kelvin.sdk.lib.common.exceptions import DependencyNotRunning, InvalidApplicationConfiguration, KDockerException
from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationInterface, ApplicationLanguage, Interface, Language
from kelvin.sdk.lib.common.models.apps.ksdk_app_setup import (
    BaseAppBuildingObject,
    BundleAppBuildingObject,
    DockerAppBuildingObject,
    KelvinAppBuildingObject,
)
from kelvin.sdk.lib.common.models.generic import KPath, OSInfo
from kelvin.sdk.lib.common.models.ksdk_docker import (
    DockerBuildEntry,
    DockerContainer,
    DockerImage,
    DockerImageNameDetails,
    DockerNetwork,
    KSDKDockerAuthentication,
    KSDKNetworkConfig,
)
from kelvin.sdk.lib.common.models.types import EmbeddedFiles, VersionStatus
from kelvin.sdk.lib.common.templates.templates_manager import get_embedded_file
from kelvin.sdk.lib.common.utils.general_utils import file_has_valid_python_requirements, standardize_string
from kelvin.sdk.lib.common.utils.logger_utils import logger
from kelvin.sdk.lib.common.utils.version_utils import assess_version_status, color_formats

if OSInfo.is_posix:
    import dockerpty


class DockerManager:
    _docker_client: APIClient
    _minimum_docker_version: Optional[str]

    def __init__(
        self,
        credentials: KSDKDockerAuthentication,
        network_configuration: KSDKNetworkConfig,
        minimum_docker_version: Optional[str] = None,
    ):
        """
        Initialises a DockerManager object based on the provided configurations.

        :param network_configuration: the object containing all the variables required to manage a docker network.
        :param credentials: the object containing all necessary credentials for docker registry interaction.
        :param minimum_docker_version: the minimum accepted docker version to run KSDK.

        """
        self._reset_docker_client()
        self._minimum_docker_version = minimum_docker_version
        self._validate_docker_version(minimum_docker_version=self._minimum_docker_version)
        # Credentials
        self._credentials = credentials
        # Setup the network configuration
        self._network_configuration = network_configuration

    def _reset_docker_client(self) -> APIClient:
        """
        Resets the client to its original state.

        :return: the internal Docker API Client in its new state.

        """
        try:
            self._docker_client = APIClient(timeout=DockerConfigs.docker_client_timeout)
        except Exception as exc:
            raise assess_docker_connection_exception(exc=exc)
        return self._docker_client

    @ensure_docker_is_running
    def _validate_docker_version(self, minimum_docker_version: Optional[str]) -> bool:
        """
        Sets up the minimum accepted docker version and matches it against the current docker version of the system.

        :param minimum_docker_version: the minimum accepted docker version, externally injected.

        :return: a boolean indicating whether or not the current docker version is supported and able to to run ksdk.
        """
        version_status = VersionStatus.UP_TO_DATE
        if minimum_docker_version:
            system_docker_version = ""
            try:
                docker_version_object = self._docker_client.version() if self._docker_client else None
            except (DockerException, Exception):
                docker_version_object = None

            if docker_version_object:
                system_docker_version = docker_version_object.get("Version", "").rsplit("-", 1)[0]

            if not system_docker_version:
                raise DependencyNotRunning(message=DockerConfigs.docker_dependency)

            version_status = assess_version_status(
                minimum_version=minimum_docker_version,
                current_version=system_docker_version,
                latest_version=system_docker_version,
            )

            if version_status == VersionStatus.UNSUPPORTED:
                docker_version_unsupported: str = """\n
                        {red}Docker version is no longer supported!{reset} \n
                        {red}Current: {current_version}{reset} → {yellow}Minimum: {minimum_version}{reset} \n
                        {green}For more information{reset}: https://docs.docker.com/engine/install/ \n
                        Please update Docker in order to proceed.
                """.format_map(
                    {
                        **color_formats,
                        "current_version": system_docker_version,
                        "minimum_version": minimum_docker_version,
                    }
                )
                raise KDockerException(message=docker_version_unsupported)

        return version_status == VersionStatus.UP_TO_DATE

    # 1 - AUTH
    @ensure_docker_is_running
    def login_on_docker_registry(self) -> Optional[APIClient]:
        """
        Logs in to the docker registry specified in the credentials object.

        :return:(s) the successfully logged instance Docker APIClient.

        """
        try:
            self._docker_client.login(
                username=self._credentials.username,
                password=self._credentials.password,
                registry=self._credentials.full_registry_url,
                reauth=True,
            )
            registry = self._credentials.full_registry_url
            logger.relevant(f'Successfully logged on registry "{registry}"')
            return self._docker_client
        except APIError as exc:
            if exc.status_code == 500:
                login_docker_registry_failure: str = f"""
                    "Error accessing the registry: {exc.explanation}. \n
                    The build process will continue regardless."
                """
                logger.warning(login_docker_registry_failure)
                return None
            raise

    # 2 - NETWORKS
    @ensure_docker_is_running
    def get_docker_network_id(self) -> str:
        """
        Get the id of the docker network specified in the instance network configuration.

        :return: the running id of the matching the network configuration.

        """
        matching_networks = self._docker_client.networks(names=[self._network_configuration.network_name])
        target_network = matching_networks[0] if matching_networks else {}
        return DockerNetwork(**target_network).id

    @ensure_docker_is_running
    def create_docker_network(self) -> bool:
        """
        Creates and launches a docker network with the specified instance configuration.

        :return: a boolean indicating whether the network was initiated.

        """
        docker_network_successfully_created = True

        network_name = self._network_configuration.network_name
        docker_network_id = self.get_docker_network_id()

        if not docker_network_id:
            result = self._docker_client.create_network(
                name=network_name, driver=self._network_configuration.network_driver, internal=False
            )
            docker_network_successfully_created = bool(result)

        if docker_network_successfully_created:
            logger.debug(f'Docker network "{network_name}" successfully started')
            return True

        raise KDockerException(message=f'Error starting docker network "{network_name}"')

    @ensure_docker_is_running
    def remove_docker_network(self) -> bool:
        """
        Removes all docker networks that correspond to the instance's network configuration.

        :return: a boolean indicating whether the specified docker networks were removed.

        """
        docker_network_name = self._network_configuration.network_name
        docker_network_id = self.get_docker_network_id()

        if docker_network_id:
            docker_containers_to_be_stopped = self.get_network_docker_containers()
            for container in docker_containers_to_be_stopped:
                self._docker_client.disconnect_container_from_network(container=container.id, net_id=docker_network_id)
                self._docker_client.stop(container.id)
            self._docker_client.remove_network(net_id=docker_network_id)
            self._docker_client.prune_networks()

        logger.debug(f'Docker network "{docker_network_name}" successfully removed')
        return True

    @ensure_docker_is_running
    def get_network_docker_containers(self) -> List[DockerContainer]:
        """
        Retrieve the ids of all docker containers running on the instance's network.

        :return: a list containing the ids of the docker containers running under the instance's network.

        """
        network_docker_containers: List[DockerContainer] = []

        matching_networks = [
            DockerNetwork(**network_obj)
            for network_obj in self._docker_client.networks(names=[self._network_configuration.network_name])
        ]

        for network in matching_networks:
            detailed_network_info = self._docker_client.inspect_network(net_id=network.id)
            container_keys = detailed_network_info.get("Containers", {}) if detailed_network_info else {}
            for key, value in container_keys.items():
                container_name = value.get("Name", "")
                container_state = value.get("State", "")
                container_is_running = container_state == "running"
                network_docker_containers.append(
                    DockerContainer(id=key, image_name=container_name, running=container_is_running)
                )

        return network_docker_containers

    # 3 - DOCKERFILES
    @staticmethod
    def build_kelvin_app_dockerfile(kelvin_app_building_object: KelvinAppBuildingObject) -> bool:
        """
        Build the docker file used in the creation of the docker image.

        :param kelvin_app_building_object: the KelvinAppBuildingObject with all the required variables to build an app.

        :return: a boolean indicating whether the dockerfile was successfully built.

        """
        # 1 - Make sure the kelvin app configuration is available
        kelvin_app = kelvin_app_building_object.app_config_model.app.kelvin
        if kelvin_app is None or kelvin_app.core is None:
            raise InvalidApplicationConfiguration(message=str(kelvin_app_building_object.app_config_file_path))

        language: Optional[Language] = kelvin_app.core.language
        if language is None:
            raise InvalidApplicationConfiguration(
                message=GeneralMessages.invalid_app_name.format(reason="Language is missing")
            )

        interface: Optional[Interface] = kelvin_app.core.interface
        if interface is None:
            raise InvalidApplicationConfiguration(
                message=GeneralMessages.invalid_app_name.format(reason="Interface is missing")
            )

        # 2 - if there is an image configuration that provides a valid system packages list, collect it.
        system_packages: str = ""
        if kelvin_app.images and kelvin_app.system_packages:
            system_packages = " ".join(kelvin_app.system_packages)

        # 3 - Verify compatibility between for both python and cpp apps.
        requirements_file = None
        app_language = language.type
        app_interface = interface.type

        if app_language == ApplicationLanguage.python:
            python_app_config = language.python
            if python_app_config:
                requirements_file = python_app_config.requirements
                if requirements_file and file_has_valid_python_requirements(file_path=KPath(requirements_file)):
                    requirements_file = KPath(requirements_file).relative_to(kelvin_app_building_object.app_dir_path)
            if app_interface is not ApplicationInterface.client:
                invalid_interface = "Invalid interface. Please provide a client type interface"
                error_message = GeneralMessages.invalid_app_name.format(reason=invalid_interface)
                raise InvalidApplicationConfiguration(message=error_message)
        if app_language == ApplicationLanguage.cpp:
            if app_interface is not ApplicationInterface.data:
                invalid_interface = "Invalid interface. Please provide a data type interface"
                error_message = GeneralMessages.invalid_app_name.format(reason=invalid_interface)
                raise InvalidApplicationConfiguration(message=error_message)

        # 4 - Retrieve the appropriate docker template for the language the app is building for.
        template = (
            EmbeddedFiles.CPP_APP_DOCKERFILE
            if app_language == ApplicationLanguage.cpp
            else EmbeddedFiles.PYTHON_APP_DOCKERFILE
        )
        dockerfile_template: Template = get_embedded_file(embedded_file=template)
        if not dockerfile_template:
            raise KDockerException(f"No template available for {app_language.value_as_str} kelvin_app_lang")

        # 5 - Prepare the dockerfile parameters and finally render the template with them as arguments.
        app_file_system_name = standardize_string(value=str(kelvin_app_building_object.app_config_model.info.name))
        dockerfile_parameters: Dict[str, Any] = {
            "build_for_data_model_compilation": kelvin_app_building_object.build_for_data_model_compilation,
            "base_data_model_builder_image": kelvin_app_building_object.base_data_model_builder_image,
            "base_image": kelvin_app_building_object.base_image,
            "app_configuration_file": kelvin_app_building_object.app_config_file_path.name,
            "app_file_system_name": app_file_system_name,
            "requirements_file": requirements_file,
            "system_packages": system_packages,
            "app_language": app_language.name,
            "app_interface": app_interface.name,
        }
        if app_language.name == "python" and app_interface.name == "client":
            if language.python:
                dockerfile_parameters.update({"entry_point": language.python.entry_point})
            if interface.client:
                dockerfile_parameters.update({"executable": interface.client.executable})

        dockerfile_content = dockerfile_template.render(dockerfile_parameters)
        kelvin_app_building_object.dockerfile_path.write_text(dockerfile_content)
        logger.debug(f"Build Dockerfile:\n\n{dockerfile_content}")
        return True

    # 4 - IMAGES
    @ensure_docker_is_running
    def build_kelvin_app_docker_image(self, kelvin_app_building_object: KelvinAppBuildingObject) -> bool:
        """
        Build the docker image from the provided KelvinAppBuildingObject.

        An exception is expected should any step of the process fail.

        :param kelvin_app_building_object: an object that contains the necessary variables to build a kelvin-type app.

        :return: a boolean indicating whether the image was successfully built.

        """
        # 1 - Login on the registry
        self.login_on_docker_registry()

        # 2 - Both the base builder image and datamodel builder images are required so we assure them
        self.ensure_base_docker_images_exist(
            base_docker_image=kelvin_app_building_object.base_image,
            base_data_model_builder=kelvin_app_building_object.base_data_model_builder_image,
        )

        return self._build_engine_step(
            base_build_object=kelvin_app_building_object,
            dockerfile_path=kelvin_app_building_object.dockerfile_path,
            docker_build_context_path=kelvin_app_building_object.docker_build_context_path,
            build_args=kelvin_app_building_object.build_args,
        )

    @staticmethod
    def build_bundle_app_dockerfile(bundle_app_building_object: BundleAppBuildingObject) -> bool:
        """
        Build the docker file used in the creation of the docker image.

        :param bundle_app_building_object: the KSDAppBuildingObject that contains
        all the required variables to build an app.

        :return: a boolean indicating whether the dockerfile was successfully built.

        """

        dockerfile_template: Template = get_embedded_file(embedded_file=EmbeddedFiles.BUNDLE_APP_DOCKERFILE)

        dockerfile_parameters: Dict[str, Any] = {
            "base_image": bundle_app_building_object.base_image,
            "base_data_model_builder_image": bundle_app_building_object.base_data_model_builder_image,
            "system_packages": " ".join(bundle_app_building_object.system_packages),
        }
        dockerfile_content = dockerfile_template.render(dockerfile_parameters)
        bundle_app_building_object.dockerfile_path.write_text(dockerfile_content)
        logger.debug(f"Build Dockerfile:\n\n{dockerfile_content}")

        return True

    @ensure_docker_is_running
    def build_docker_app_image(self, docker_build_object: DockerAppBuildingObject) -> bool:
        """
        Build the docker image from the provided DockerAppBuildingObject.

        An exception is expected should any step of the process fail.

        :param docker_build_object: an object that contains the necessary variables to build a docker-type app.

        :return: a boolean indicating whether the image was successfully built.

        """
        dockerfile_path: Optional[KPath]
        docker_build_context_path: Optional[KPath]
        build_args = {}

        # 1 - Make sure the kelvin app configuration is available
        docker_app = docker_build_object.app_config_model.app.docker
        if not docker_app:
            raise InvalidApplicationConfiguration(message=str(docker_build_object.app_config_file_path))

        # 2 - Parse the docker parameters depending on the type.
        # 2.1 - If it has both a base image and the entrypoint, assume those
        if docker_app.image:
            dockerfile: str = DockerConfigs.default_dockerfile_content_with_entrypoint
            if docker_app.entrypoint:
                clean_entrypoint = json.dumps(docker_app.entrypoint)
                dockerfile = dockerfile.format(base_image=docker_app.image, entrypoint=clean_entrypoint)
            else:
                dockerfile = DockerConfigs.default_dockerfile_content_base.format(base_image=docker_app.image)
            dockerfile_path = KPath(docker_build_object.app_build_dir_path / GeneralConfigs.default_dockerfile)
            dockerfile_path.write_content(content=dockerfile)
            docker_build_context_path = docker_build_object.app_dir_path
        # 2.2 - If not, check if there's a build configuration
        elif docker_app.build:
            build_config = docker_app.build
            dockerfile_path = KPath(build_config.dockerfile)
            docker_build_context_path = KPath(build_config.context)
            if build_config.args:
                split_args = (arg.split("=") for arg in build_config.args)
                build_args = {key: value for key, value in split_args}
        # 2.3 - If none of the past 2 scenarios is respect, assume nothing was provided.
        else:
            raise InvalidApplicationConfiguration(message=str(docker_build_object.app_config_file_path))

        return self._build_engine_step(
            base_build_object=docker_build_object,
            dockerfile_path=dockerfile_path,
            docker_build_context_path=docker_build_context_path,
            build_args=build_args,
        )

    def _build_engine_step(
        self,
        base_build_object: BaseAppBuildingObject,
        dockerfile_path: KPath,
        docker_build_context_path: KPath,
        build_args: Optional[Dict[str, str]],
    ) -> bool:
        """
        Internal method shared by both kelvin and docker apps in order to build.

        :param base_build_object: the base building object with the necessary inputs.
        :param dockerfile_path: the path to the dockerfile
        :param docker_build_context_path: the path to where the docker build should be executed (context).
        :param build_args: additional build arguments to be passed to the build operation.

        :return: a boolean indicating the build step was successfully executed.

        """
        docker_image_name = base_build_object.full_docker_image_name  # name of the docker image
        docker_image_labels = base_build_object.docker_image_labels  # ksdk identification labels
        dockerfile_path_relative_to_context = PurePosixPath(dockerfile_path.relative_to(docker_build_context_path))
        build_log_file = GeneralConfigs.default_build_logs_file
        docker_build_complete_stack: List[DockerBuildEntry] = []
        docker_stack_trace_has_errors: bool = False

        # 3 - Fresh applications attempt to purge all the existing cache
        if base_build_object.fresh_build:
            self.prune_docker_containers()
            self.prune_docker_images()

        # 4 - If its a 'rebuild', stop all existing containers of this same app
        if self.check_if_docker_image_exists(docker_image_name=docker_image_name):
            # 5 - If its an 'appregistry upload', purge any previous instance and start from scratch
            if base_build_object.fresh_build or base_build_object.build_for_upload:
                self.remove_docker_image(docker_image_name=docker_image_name)
            else:
                self.stop_docker_containers_for_image(docker_image_name=docker_image_name)

        # 6 - Build the image and store the logs
        logger.info(f'Building new image for "{docker_image_name}". Please wait..')
        for entry in self._docker_client.build(
            path=str(docker_build_context_path),
            dockerfile=str(dockerfile_path_relative_to_context),
            tag=docker_image_name,
            labels=docker_image_labels,
            buildargs=build_args,
            rm=True,
            decode=True,
        ):
            # 6.1 - Store all log output entries
            dockerfile_build_entry = DockerBuildEntry(**entry)
            docker_build_complete_stack.append(dockerfile_build_entry)
            # 6.2 - If there are any errors, collect them as well
            docker_stack_trace_has_errors |= dockerfile_build_entry.entry_has_errors
            # 6.3 output the verbose entries to the debug level
            verbose_entry = process_dockerfile_build_entry(entry=entry)
            if verbose_entry:
                logger.debug(verbose_entry)

        # 7 - Once built, tag the image to have a 'latest' version
        if self.check_if_docker_image_exists(docker_image_name=docker_image_name):
            self._docker_client.tag(
                image=docker_image_name,
                repository=base_build_object.docker_image_name,
                tag=DockerConfigs.latest_docker_image_version,
            )

        # 8 - Output the complete Dockerfile and respective logs to the build/build.log file
        build_logs_file: KPath = dockerfile_path.parent / build_log_file
        if not build_logs_file.parent.exists():
            build_logs_file.parent.mkdir()

        log_file_content = KPath(dockerfile_path).read_text() + "\n"
        log_file_content += "\n".join([entry.log_content for entry in docker_build_complete_stack])
        build_logs_file.write_content(content=log_file_content)

        logger.debug(f'Build logs successfully registered on "{build_logs_file}"')

        # 9 - Raise an exception if there is any error in the stack
        if docker_stack_trace_has_errors:
            handle_error_stack_trace(complete_stack=docker_build_complete_stack)
        return True

    @ensure_docker_is_running
    def run_app_docker_image(
        self,
        docker_image_name: str,
        host_config: HostConfig,
        app_config_path: Optional[str] = None,
        net_alias: Optional[str] = None,
        entrypoint: Optional[str] = None,
        environment_variables: Optional[Dict] = None,
        arguments: Optional[str] = None,
        attach: bool = False,
    ) -> bool:
        """
        Run the specified App docker image with the provided command as argument.

        :param docker_image_name: the name of the docker image to be checked.
        :param host_config: the configuration object that configures container exposure to the host.
        :param app_config_path: the path to the app configuration file.
        :param net_alias: the network alias.
        :param entrypoint: if specified, will override the existing entrypoint of the image.
        :param environment_variables: additional environment variables to be passed on to the docker image.
        :param arguments: arguments to pass to the docker image.
        :param attach: if set, will attach to the existing container and run it interactively.

        :return: a boolean indicating whether the image exists on the local docker list.

        """
        # 1 - Getting both container's name in the network and the network id to run the container on
        docker_image_name_details = DockerImageNameDetails(
            registry_url=docker_image_name, docker_image_name=docker_image_name
        )
        container_name_in_the_network = docker_image_name_details.container_name
        docker_network_id = self.get_docker_network_id()

        # 2 - Assess if its a normal app or if it has a custom entrypoint
        if not entrypoint:
            # 2.1 - In case its a normal app, stop its running instances and remove them before advancing
            self.stop_docker_containers_for_image(docker_image_name=docker_image_name)
            self.remove_container(container=container_name_in_the_network)
        else:
            container_name_in_the_network += f"-{randint(0, 1 << 16)}"  # nosec
            logger.info(f'Running container: "{container_name_in_the_network}"')

        # 3 - Create the container with the provided configurations
        container_result = self._docker_client.create_container(
            image=docker_image_name,
            detach=False,
            host_config=host_config,
            name=container_name_in_the_network,
            entrypoint=entrypoint,
            stdin_open=attach,
            environment=environment_variables,
            command=arguments,
            tty=attach,
        )
        container = DockerContainer(id=container_result.get("Id", ""), image_name=docker_image_name)

        # 4 - If there is a app configuration, insert it into the container
        if app_config_path and container_result:
            app_container_app_dir_path = KPath(DockerConfigs.app_container_app_dir_path)
            app_config_override = self.add_file_to_container(
                container_id=container.id,
                file_path=KPath(app_config_path),
                container_file_path=app_container_app_dir_path,
            )
            if app_config_override:
                logger.relevant(f'Overriding existing configuration with "{app_config_path}"')

        # 5 - Connect the newly created container to the docker network
        aliases = [net_alias] if net_alias is not None else None

        self._docker_client.connect_container_to_network(
            container=container.id, net_id=docker_network_id, aliases=aliases
        )
        logger.debug("Container connected to the network")

        # 6 - Jumpstart the app
        if attach:
            # 6.1 - If it is an interactive session (attach), start it with dockerpty (windows excluded)
            if not OSInfo.is_posix:
                logger.error("Attaching an interactive session on Windows is not supported")
                return False
            dockerpty.start(self._docker_client, container_result)
        else:
            # 6.2 - If not, just start the container and attempt to load its logs (if that's the case)
            self._docker_client.start(container=container.id)
            self._display_container_logs(container=container, is_a_test_run=bool(entrypoint))
            logger.debug(f'Container "{container.id}" ("{docker_image_name}") successfully started')

        return True

    @ensure_docker_is_running
    def ensure_base_docker_images_exist(self, base_docker_image: str, base_data_model_builder: str) -> bool:
        """
        Using the base logged client, ensure that the provided images are valid in the currently logged registry.

        :param base_docker_image: the docker image used to build the application.
        :param base_data_model_builder: the docker image used to compile datamodels.

        :return: a boolean indicating whether the images are valid in the currently logged registry.
        """
        for image_name in [base_docker_image, base_data_model_builder]:
            try:
                self.pull_docker_image_from_registry(docker_image_name=image_name)
            except NotFound as exc:
                # 1 - if does not exist in the registry, look for it locally.
                if not self.check_if_docker_image_exists(docker_image_name=image_name, all_images=True):
                    raise exc
        return True

    @ensure_docker_is_running
    def push_docker_image_to_registry(self, docker_image_name: str) -> bool:
        """
        Push the specified docker image to the currently logged registry.

        :param docker_image_name: the name of the docker image to building.

        :return: a boolean indicating whether the image was successfully pushed to the currently logged registry.

        """
        image_name_details = DockerImageNameDetails(
            docker_image_name=docker_image_name, registry_url=self._credentials.full_registry_url
        )
        docker_image_name_for_registry = image_name_details.repository_docker_image_name

        if not self._docker_client.tag(docker_image_name, docker_image_name_for_registry, force=True):
            raise KDockerException(f"Error tagging {docker_image_name} to {docker_image_name_for_registry}")

        # Pushing operation
        auth_config: dict = {"username": self._credentials.username, "password": self._credentials.password}

        stream = self._docker_client.push(docker_image_name_for_registry, auth_config=auth_config, stream=True)

        # Display all the information from the stream
        display_docker_progress(stream=stream)

        # Once pushed, remove the docker image and proceed.
        return self.remove_docker_image(docker_image_name=docker_image_name_for_registry)

    @ensure_docker_is_running
    def pull_docker_image_from_registry(self, docker_image_name: str, override_local_tag: bool = False) -> bool:
        """
        Pull the specified docker image from the currently logged registry.

        :param docker_image_name: the name of the docker image to be pulled.
        :param override_local_tag: if set, will indicate whether the pulled image should override the local tag.

        :return: a boolean indicating whether the image was successfully pulled to the currently logged registry.

        """
        auth_config = {"username": self._credentials.username, "password": self._credentials.password}

        # will yield a string with the format "<client>.kelvininc.com:5000/<image-name>:<image-version>"
        image_name_details = DockerImageNameDetails(
            docker_image_name=docker_image_name, registry_url=self._credentials.full_registry_url
        )
        docker_image_name_for_registry = image_name_details.repository_docker_image_name

        logger.info(f'Pulling "{docker_image_name}" from "{self._credentials.registry_url}"')

        try:
            stream = self._docker_client.pull(
                repository=docker_image_name_for_registry, auth_config=auth_config, stream=True
            )
            # Get both image names and version
            image_name, image_version = image_name_details.image_name_and_version
            # Display the stream progress
            display_docker_progress(stream=stream)
            logger.relevant(f'Successfully pulled "{docker_image_name}" from "{self._credentials.registry_url}"')
            if override_local_tag:
                self._docker_client.tag(
                    image=docker_image_name_for_registry, repository=image_name, tag=image_version, force=True
                )
        except NotFound:
            raise NotFound(
                f"""\n
                The provided app is not available in the platform's registry: \"{docker_image_name_for_registry}\". \n
                Please provide a valid combination of image and version. E.g \"hello-world:0.0.1\" \n
            """
            )
        except Exception as exc:
            raise KDockerException(message=f'Error pulling "{docker_image_name}": {str(exc)}')

        return True

    @ensure_docker_is_running
    def remove_docker_image(self, docker_image_name: str, silent: bool = False) -> bool:
        """
        Remove the specified docker image from the local system.

        Raise an exception if the docker image was not successfully removed.

        :param docker_image_name: the name of the docker image to be removed.
        :param silent: indicates whether logs should be displayed.

        :return: a boolean indicating whether the image was successfully removed.

        """
        # 1 - Check if the image exists. If not, raise the proper exception
        matching_images = self.get_docker_images(docker_image_name=docker_image_name)

        if not matching_images:
            raise KDockerException(f'Image "{docker_image_name}" does not exist')

        for image in matching_images:
            for tag in image.tags:
                # 2 - Stop the containers for the provided image
                self.stop_docker_containers_for_image(docker_image_name=tag)

                # 3 - attempt to remove the image
                docker_image_was_removed = self._docker_client.remove_image(tag, force=True)

                # 4 - transform the docker image result to a string
                removed_result_str = str(docker_image_was_removed) if docker_image_was_removed else None

                # 5 - verify if the success string is part of the result
                docker_image_was_removed = removed_result_str is not None and tag in removed_result_str

                if not docker_image_was_removed:
                    raise KDockerException(f'Error removing "{tag}"')

                if not silent:
                    logger.info(f'Image "{tag}" successfully removed')

        return True

    @ensure_docker_is_running
    def prune_docker_images(self, filters: dict = None) -> bool:
        """
        A simple wrapper around the client to prune dangling docker images.

        :param filters: the keywords used to filter out the prune operation.

        :return: a bool indicating the images were successfully pruned.
        """
        try:
            self._docker_client.prune_images(filters=filters)
            logger.debug("Images successfully pruned")
            return True
        except Exception:
            raise KDockerException("Error pruning images")

    @ensure_docker_is_running
    def check_if_docker_image_exists(
        self, docker_image_name: str, silent: bool = False, labels: Optional[dict] = None, all_images: bool = False
    ) -> bool:
        """
        Check whether the specified docker image exists on the local system.

        :param docker_image_name: the name of the docker image to be checked.
        :param silent: indicates whether logs should be displayed.
        :param labels: the labels to apply on the filter operation.
        :param all_images: if set to True, will bypass the labels and retrieve all images.

        :return: a boolean indicating whether the image exists on the local docker list.

        """
        docker_images = self.get_docker_images(
            docker_image_name=docker_image_name, labels=labels, all_images=all_images
        )
        if not silent:
            if docker_images:
                message = f'Image "{docker_image_name}" already exists'
            else:
                message = f'Image "{docker_image_name}" does not exist'
            logger.debug(message)

        return bool(docker_images)

    @ensure_docker_is_running
    def get_docker_images(
        self, docker_image_name: Optional[str] = None, labels: Optional[dict] = None, all_images: bool = False
    ) -> List[DockerImage]:
        """
        Return the list of all docker images in the local system.

        This image list can be narrowed down by using labels or an image name.
        By default, includes the standard: {'source': 'ksdk'} labels.

        :param docker_image_name: the name of the docker image to be matched.
        :param labels: the labels used to get images. If not specified, will provide all the ksdk defaults.
        :param all_images: if set to 'True', will bypass the labels and retrieve all images.

        :return: a list of DockerImage items.
        """
        identification_labels: dict = DockerConfigs.ksdk_base_identification_label

        if labels:
            if "name" in labels:
                labels.pop("name", "")
            identification_labels = labels

        docker_images = self._docker_client.images()

        all_docker_images: List[DockerImage] = []
        for image in docker_images:
            image_id = image.get("Id", "")
            image_parent_id = image.get("ParentId", "")
            image_tags = image.get("RepoTags", []) or []
            image_created = image.get("Created", "")
            image_labels: dict = image.get("Labels", {}) or {}
            image_entry = DockerImage(
                id=image_id,
                parent_id=image_parent_id,
                tags=image_tags,
                created=image_created,
                labels=image_labels,
            )
            all_docker_images.append(image_entry)

        if not all_images:
            filtered_images: List[DockerImage] = []
            for image in all_docker_images:
                labels_match = identification_labels.items() <= image.labels.items()
                matches_image_name = docker_image_name is None or docker_image_name in image.tags
                if all_images or (labels_match and matches_image_name):
                    filtered_images.append(image)
            return filtered_images

        return all_docker_images

    @ensure_docker_is_running
    def unpack_app_from_docker_image(
        self,
        app_name: str,
        output_dir: str,
        image_dir: str = DockerConfigs.app_container_app_dir_path,
        clean_dir: bool = True,
    ) -> bool:
        """
        Extract the content of the specified built application to the provided output directory.

        :param app_name: the name of the application to unpack.
        :param output_dir: the directory into which the application will be unpacked.
        :param image_dir: the directory from which to extract the application content.
        :param clean_dir: clean the directory before extracting into it.

        :return: a boolean flag indicating the image was successfully unpacked.

        """
        default_unpack_app_name = "unpack"

        output_dir_path = KPath(output_dir)
        if clean_dir:
            output_dir_path.delete_dir().create_dir()
        else:
            output_dir_path.create_dir()

        self.remove_container(container=default_unpack_app_name)

        container = self._docker_client.create_container(
            image=app_name,
            stdin_open=True,
            name=default_unpack_app_name,
            entrypoint="tail",
            command=["-f", "/dev/null"],
        )
        container_object = DockerContainer(id=container.get("Id", ""), image_name=default_unpack_app_name)

        bundle_folder_extracted: bool = False

        # try to extract application type app
        app_folder_extracted: bool = self.extract_folder_from_container(
            container_id=container_object.id, folder=image_dir, output_dir=output_dir
        )

        if not app_folder_extracted:
            # try to extract application type bundle
            bundle_image_dir = DockerConfigs.app_bundle_dir_path
            bundle_folder_extracted = self.extract_folder_from_container(
                container_id=container_object.id, folder=bundle_image_dir, output_dir=output_dir
            )

        if not (app_folder_extracted or bundle_folder_extracted):
            logger.warning("The application unpack feature is not compatible with this application type")

        self._docker_client.remove_container(container=default_unpack_app_name)

        return app_folder_extracted or bundle_folder_extracted

    def extract_folder_from_container(self, container_id: str, folder: str, output_dir: str) -> bool:
        unpack_temp_file = "app.tar"
        app_container_app_dir = DockerConfigs.app_container_app_dir

        try:
            stream, stat = self._docker_client.get_archive(container=container_id, path=folder)
            with TemporaryDirectory(dir=OSInfo.temp_dir) as temp_dir:
                app_tar_file = KPath(temp_dir) / unpack_temp_file

                with open(app_tar_file, "wb") as f:
                    for item in stream:
                        f.write(item)

                with tarfile.TarFile(app_tar_file) as tf:
                    for member in tf.getmembers():
                        if member.name.startswith(f"{app_container_app_dir}/"):
                            member.name = str(Path(member.name).relative_to(app_container_app_dir))
                    tf.extractall(path=output_dir)
        except DockerException:
            return False

        return True

    # 5 - CONTAINERS
    @ensure_docker_is_running
    def get_docker_containers(
        self, docker_image_name: Optional[str] = None, labels: Optional[dict] = None, all_containers: bool = False
    ) -> List[DockerContainer]:
        """
        Obtain a list of all docker containers available in the system.

        This image list can be narrowed down by using labels or an image name.
        By default, includes the standard: {'source': 'ksdk'} labels.

        :param docker_image_name: the name of the docker image to filters the containers.
        :param labels: the labels used to selectively get containers.
        :param all_containers: if set to 'True', will bypass all requirements and retrieve all containers.

        :return: a list of DockerContainer items.

        """
        identification_labels: dict = DockerConfigs.ksdk_base_identification_label

        if labels:
            if "name" in labels:
                labels.pop("name", "")
            identification_labels = labels

        docker_containers = self._docker_client.containers(all=True)

        container_name: Optional[str] = None
        if docker_image_name:
            image_details = DockerImageNameDetails(registry_url=docker_image_name, docker_image_name=docker_image_name)
            container_name = image_details.container_name

        all_docker_containers: List[DockerContainer] = []
        for container in docker_containers:
            container_id = container.get("Id", "")
            container_names: List[str] = [name.replace("/", "") for name in container.get("Names", []) or []]
            container_image = container.get("Image", "")
            container_is_running = container.get("State", "") == "running"
            container_labels: dict = container.get("Labels", {}) or {}
            container_ports: List = container.get("Ports", [])

            container_network_settings: dict = container.get("NetworkSettings", {})
            container_networks: dict = container_network_settings.get("Networks", {})
            container_network_ksdk: dict = container_networks.get(DockerConfigs.default_ksdk_network, {})
            container_network_ip: str = container_network_ksdk.get("IPAddress", "")

            container_entry = DockerContainer(
                id=container_id,
                container_names=[name.replace("/", "") for name in container_names],
                image_name=container_image,
                id_address=container_network_ip,
                running=container_is_running,
                ports=container_ports,
                labels=container_labels,
            )
            all_docker_containers.append(container_entry)

        if not all_containers:
            filtered_containers: List[DockerContainer] = []
            for container in all_docker_containers:
                labels_match = not container.labels or identification_labels.items() <= container.labels.items()
                matches_image_name = docker_image_name is None or docker_image_name == container.image_name
                matches_container_name = container_name is None or container_name in container.container_names
                if labels_match and (matches_image_name or matches_container_name):
                    filtered_containers.append(container)
            return filtered_containers

        return all_docker_containers

    @ensure_docker_is_running
    def get_container_host_config(
        self, binds: List[str], port_mapping: Dict, auto_remove: bool = False, publish_all_ports: bool = True
    ) -> HostConfig:
        """
        Return the default HostConfig for both the network and running containers.

        :param binds: the binds object that indicates which volumes should be exposed between
        the container and the host.
        :param port_mapping: the ports to be mapped between the container and the host machine.
        :param auto_remove: indicates whether the container should be removed upon stop.
        :param publish_all_ports: indicates whether all ports should be exposed between the container and host.

        :return: a HostConfig object.

        """
        return self._docker_client.create_host_config(
            binds=binds or [],
            port_bindings=port_mapping or {},
            auto_remove=auto_remove,
            publish_all_ports=publish_all_ports,
        )

    @ensure_docker_is_running
    def add_file_to_container(self, container_id: str, file_path: KPath, container_file_path: KPath) -> bool:
        """
        Copy the provided file into a container.

        :para container: the id of the container to add the file into.
        :para file_path: the path of the file to be added.
        :para container_file_path: the path of the file inside the container.

        :return: a boolean indicating whether the file was successfully added to the container.
        """
        import time
        from io import BytesIO

        file_tar_stream = BytesIO()

        file_tar = tarfile.TarFile(fileobj=file_tar_stream, mode="w")
        with open(file_path.absolute(), "rb") as file:
            file_data = file.read()

        tarinfo = tarfile.TarInfo(name=file_path.name)
        tarinfo.size = len(file_data)
        tarinfo.mtime = int(time.time())

        file_tar.addfile(tarinfo, BytesIO(file_data))
        file_tar.close()
        file_tar_stream.seek(0)

        config_file_exists: bool = True
        try:
            self._docker_client.get_archive(container=container_id, path=container_file_path)
        except DockerException:
            config_file_exists = False

        return config_file_exists and self._docker_client.put_archive(
            container=container_id, path=container_file_path, data=file_tar_stream.read()
        )

    @ensure_docker_is_running
    def stop_docker_containers_for_image(self, docker_image_name: str) -> bool:
        """
        Stop all the containers of the specified image.

        :param docker_image_name: the name of docker image whose containers should be stopped.

        :return: a symbolic return boolean.

        """
        containers_for_image_name = self.get_docker_containers(docker_image_name=docker_image_name)

        logger.info(f'Stopping containers of "{docker_image_name}"')
        if containers_for_image_name:
            for container in containers_for_image_name:
                self._docker_client.stop(container=container.id)
            logger.info(f'Containers of "{docker_image_name}" successfully stopped')
            return True
        else:
            return False

    @ensure_docker_is_running
    def remove_container(self, container: str) -> bool:
        """
        Remove the provided container from the system.

        :param container: the id of the container to be removed.

        :return: a default boolean indicating the container removal operation was successful.

        """
        all_containers = self.get_docker_containers(all_containers=True)  # include the stopped ones as well

        matching_container = [entry for entry in all_containers if container in entry.container_names]
        if matching_container:
            self._docker_client.remove_container(container=container, force=True)

        logger.debug("Container successfully removed")

        return True

    @ensure_docker_is_running
    def get_logs_for_docker_container(self, docker_image_name: str, tail: bool = False) -> bool:
        """
        Prints out the logs of the containers of the specified docker image.

        :param docker_image_name: the name of the docker image whose container is to be logged.
        :param tail: if set to 'True', will tail the logs and return.

        :return: a symbolic return flag.

        """
        containers = self.get_docker_containers(docker_image_name=docker_image_name) or []

        for docker_container in containers:
            logs = self._docker_client.attach(
                container=docker_container.id, stdout=True, stderr=True, stream=(not tail), logs=True
            )
            try:
                if tail:
                    logs = logs.decode().split("\n")
                    for item in logs:
                        print(item)  # noqa
                else:
                    for item in logs:
                        print(item.decode("utf-8"), end="")  # noqa
            except Exception as exc:
                logger.error(f'Error processing logs: "{str(exc)}"')
            return True
        return False

    @ensure_docker_is_running
    def prune_docker_containers(self, filters: dict = None) -> bool:
        """
        A simple wrapper around the client to prune dangling docker containers.

        :param filters: the keywords used to filter out the prune operation.

        :return: a symbolic return flag.

        """
        try:
            self._docker_client.prune_containers(filters=filters)
            logger.debug("Containers successfully pruned")
            return True
        except (DockerException, Exception):
            raise KDockerException("Error pruning docker containers. Proceeding.")

    def _display_container_logs(self, container: DockerContainer, is_a_test_run: bool = False) -> bool:
        """
        Display the containers of the provided container.
        If it is a test run, display the logs regardless of the status code.

        :param container: the container to display the logs of.
        :param is_a_test_run: indicates whether the container is merely executing app tests.

        :return: return a boolean indicating whether the container log data was successfully displayed.

        """
        try:
            # 1 - raise an exception if its a Windows machine. Windows is not supported for this operation.
            if not OSInfo.is_posix:
                raise SystemError("Skipping error code retrieval")

            # 2 - Set a timeout for log retrieval.
            timeout = 3 if not is_a_test_run else None
            res = self._docker_client.wait(container=container.id, timeout=timeout)
            if res:
                status_code = res.get("StatusCode", None)
                if status_code:
                    error_log = self._docker_client.logs(container=container.id)
                    error_stack = error_log.decode("utf8")
                    raise KDockerException(f"{error_stack}\n\nApplication stopped with error code: {status_code}")
                elif is_a_test_run:
                    test_log = self._docker_client.logs(container=container.id)
                    test_log_stack = test_log.decode("utf8")
                    logger.info(test_log_stack)
        except KDockerException:
            # Up-forward catch the intentionally raised exception
            raise
        except Exception:
            return False
        return True
