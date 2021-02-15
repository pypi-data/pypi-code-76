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
from typing import TYPE_CHECKING, Dict, List, Optional

from kelvin.sdk.client.error import APIError
from kelvin.sdk.lib.common.auth.auth_manager import login_client_on_current_url
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.models.apps.common import Version
from kelvin.sdk.lib.common.models.apps.kelvin_app import IO, Connection, DataModel
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import KelvinAppConfiguration
from kelvin.sdk.lib.common.models.factories.app_setup_configuration_objects_factory import (
    get_legacy_app_building_object,
)
from kelvin.sdk.lib.common.models.generic import KPath
from kelvin.sdk.lib.common.models.legacy.ksdk_app_configuration import LegacyEnvironmentConfiguration
from kelvin.sdk.lib.common.models.types import EmbeddedFiles
from kelvin.sdk.lib.common.templates.templates_manager import get_embedded_file
from kelvin.sdk.lib.common.utils.general_utils import get_system_requirements_from_file
from kelvin.sdk.lib.common.utils.logger_utils import logger

if TYPE_CHECKING:
    from kelvin.sdk.lib.common.models.legacy.ksdk_app_configuration import LegacyAppIO


def migrate_app_configuration(app_dir_path: str, output_file_path: KPath) -> Optional[KelvinAppConfiguration]:
    """
    When provided with a path to an old project, return the migrated, corresponding KelvinAppConfiguration.

    :param app_dir_path: the path to the directory that holds the outdated app.
    :param output_file_path: the output file path where the new configuration should be written.

    :return: a new, up-to-date KelvinAppConfiguration object.

    """

    legacy_build_object = get_legacy_app_building_object(app_dir=app_dir_path)
    legacy_app_config_model = legacy_build_object.app_config_model

    app_configuration = legacy_app_config_model.configuration
    info_object = legacy_app_config_model.info.dict()

    # build interface
    descriptor = app_configuration.descriptor

    interface = {
        "client": {"args": [], "executable": "run_app", "period": descriptor.period, "spawn": True},
        "type": "client",
    }

    # extract system requirements from file
    system_requirements_path = KPath(app_dir_path) / GeneralConfigs.default_system_packages_file
    system_requirements = get_system_requirements_from_file(system_requirements_path)

    # convert entrypoint to python module path
    package_entry_point = migrate_legacy_entry_point(legacy_app_config_model.info.entry_point)

    # convert legacy string datamodels to Datamodel instances
    datamodels_folder = legacy_build_object.app_datamodel_dir_path
    data_models_from_app_yaml: List[DataModel] = migrate_data_models_config(legacy_app_config_model.datamodels)
    migrated_datamodels = migrate_legacy_datamodels(datamodels_folder)

    for datamodel in data_models_from_app_yaml:
        for migrated_datamodel in migrated_datamodels:
            if str(datamodel.name) == str(migrated_datamodel.name):
                datamodel.path = migrated_datamodel.path

    inputs = migrate_legacy_app_ios(legacy_app_config_model.inputs)
    outputs = migrate_legacy_app_ios(legacy_app_config_model.outputs)

    environment_path: KPath = KPath(app_dir_path) / "environment.yaml"
    environment_config_model = LegacyEnvironmentConfiguration(**environment_path.read_yaml())
    connections = migrate_connections(environment_config_model)

    app_object = {
        "type": "kelvin",
        "kelvin": {
            "core": {
                "version": "4.0.0",
                "language": {
                    "type": legacy_app_config_model.info.platform,
                    legacy_app_config_model.info.platform: {
                        "entry_point": package_entry_point,
                        "requirements": legacy_build_object.requirements_file,
                    },
                },
                "interface": interface,
                "data_models": data_models_from_app_yaml,
                "inputs": inputs,
                "outputs": outputs,
                "connections": connections,
            },
            "images": {"base": "", "builder": ""},
            "system_packages": system_requirements,
        },
    }

    kelvin_app_configuration_object = {
        "app": app_object,
        "info": info_object,
        "spec_version": "1.0.0",
    }

    kelvin_app_configuration = KelvinAppConfiguration(**kelvin_app_configuration_object)
    logger.info("New application configuration successfully loaded")

    kelvin_app_configuration.to_file(path=output_file_path)

    # Update requirements
    requirements_path: KPath = KPath(app_dir_path) / GeneralConfigs.default_requirements_file
    if requirements_path.exists():
        update_requirements(requirements_path)

    # migrate .gitignore
    gitignore_template = get_embedded_file(EmbeddedFiles.PYTHON_APP_GITIGNORE)
    gitfile_content = gitignore_template.render()
    gitfile_path = KPath(app_dir_path) / GeneralConfigs.default_git_ignore_file
    gitfile_path.write_text(gitfile_content)

    # migrate .dockerignore
    dockerignore_template = get_embedded_file(EmbeddedFiles.DOCKERIGNORE)
    dockerfile_content = dockerignore_template.render()
    dockerfile_path = KPath(app_dir_path) / GeneralConfigs.default_docker_ignore_file
    dockerfile_path.write_text(dockerfile_content)

    # clean unused files
    system_requirements_path.remove()
    environment_path.remove()

    return kelvin_app_configuration


def update_requirements(requirements_path: KPath) -> None:
    new_file_content = ""
    with open(requirements_path, "r") as file:
        file_content = file.read()

        # test if kelvin app exists
        if "kelvin-app" not in file_content:
            # add if doesn't exist
            new_file_content = file_content
            new_file_content += f"\n{GeneralConfigs.default_kelvin_app_dependency}"
        else:
            # if there is kelvin-app in requirements.txt replace with the latest
            for line in file_content.splitlines():
                stripped_line = line.strip()

                # check if the line that contains kelvin-app
                if "kelvin-app" in stripped_line:
                    new_file_content += f"\n{GeneralConfigs.default_kelvin_app_dependency}"
                else:
                    new_file_content += f"\n{stripped_line}"

    # check if pytest exists
    if "pytest" not in new_file_content:
        new_file_content += f"\npytest"

    with open(requirements_path, "w+") as file:
        file.write(new_file_content)


def migrate_legacy_entry_point(legacy_entry_point: str) -> str:
    return legacy_entry_point.replace(".py", ":App").replace("/", ".")


def migrate_legacy_datamodels(datamodels_dir: KPath) -> List[DataModel]:
    data_models: List[DataModel] = []

    files = datamodels_dir.rglob("*")
    for file in files:
        if file.suffix in [".yaml", ".yml"]:
            data_model_path = KPath(file)
            content = data_model_path.read_yaml()
            try:
                legacy_message_field = content.get("message", {})

                name = migrate_legacy_data_model_namespace_uri(content.get("namespace-uri", ""))
                version = content.get("version", "")
                if "raw" not in name:
                    migrated_datamodel_data = {
                        "fields": legacy_message_field.get("fields", {}),
                        "class_name": legacy_message_field.get("class_name", ""),
                        "description": legacy_message_field.get("description", ""),
                        "name": name,
                        "version": version,
                    }
                    data_model_path.write_yaml(migrated_datamodel_data)
                    migrated_datamodel: DataModel = DataModel(
                        name=name,
                        version=version,
                        path=str(data_model_path),
                    )
                    data_models.append(migrated_datamodel)
                else:
                    logger.warning(f"Raw datamodel detected {data_model_path}. Skipping..")
            except Exception:
                logger.warning(f"Couldn't migrate datamodel {data_model_path}.")

    return data_models


def migrate_data_models_config(legacy_datamodels: Optional[List[str]]) -> List[DataModel]:
    data_models: List[DataModel] = []
    if legacy_datamodels:
        client = login_client_on_current_url()
        for legacy_datamodel in legacy_datamodels:
            try:
                datamodel = migrate_legacy_data_model_name_with_version(legacy_datamodel)
                # get datamodel latest version from remote, otherwise use the provided version
                if "raw" in str(datamodel.name):
                    try:
                        remote_datamodel = client.data_model.get_data_model_latest_version(
                            data_model_name=datamodel.name
                        )
                        datamodel.version = Version(__root__=remote_datamodel.version)
                    except APIError:
                        logger.warning(f"Error download raw datamodel version. Using version {datamodel.version}.")

                data_models.append(datamodel)
            except (TypeError, KeyError, ValueError):
                logger.warning(f"Cannot parse datamodel {legacy_datamodel}. Skipping..")

    return data_models


def migrate_legacy_data_model_namespace_uri(legacy_name: str) -> str:
    return legacy_name.replace("http://kelvininc.com/", "").replace("/", ".")


def migrate_legacy_data_model_name_with_version(legacy_datamodel: str) -> DataModel:
    legacy_datamodel_name, version = legacy_datamodel.rsplit(":", 1)
    name = migrate_legacy_data_model_namespace_uri(legacy_datamodel_name)

    return DataModel(name=name, version=version)


def migrate_legacy_app_ios(app_ios: Dict[str, "LegacyAppIO"]) -> List[IO]:
    return [IO(name=name, data_model=app_io.type) for name, app_io in app_ios.items()]


def migrate_connections(environment_config_model: "LegacyEnvironmentConfiguration") -> List[Connection]:
    legacy_inputs = environment_config_model.bindings.inputs
    legacy_outputs = environment_config_model.bindings.outputs

    # parse and group inputs and outputs by endpoint

    inputs_endpoints = [str(legacy_input.endpoint) for legacy_input in legacy_inputs]
    outputs_endpoints = [str(legacy_output.endpoint) for legacy_output in legacy_outputs]
    endpoints: List[str] = list(set(inputs_endpoints + outputs_endpoints))
    connections: List[Connection] = []

    for index, endpoint in enumerate(endpoints):
        endpoint_inputs = [
            {"name": legacy_input.target, "node": legacy_input.source}
            for legacy_input in legacy_inputs
            if str(legacy_input.endpoint) == endpoint
        ]
        endpoint_outputs = [
            {"name": legacy_output.source, "node": legacy_output.target}
            for legacy_output in legacy_outputs
            if str(legacy_output.endpoint) == endpoint
        ]

        connection = Connection(
            name=f"myconnection-{index}",
            opcua={
                "registry_map": {
                    "inputs": endpoint_inputs,
                    "outputs": endpoint_outputs,
                },
                "endpoint": endpoint,
            },
        )
        connections.append(connection)

    return connections
