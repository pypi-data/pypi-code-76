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
from typing import Any, Dict, Optional, Tuple

import jsonschema
import requests
from jsonschema import Draft7Validator, validators

from kelvin.sdk.lib.common.configs.internal.schema_manager_configs import SchemaManagerConfigs
from kelvin.sdk.lib.common.exceptions import (
    ContentDoesNotMatchSchemaException,
    InvalidApplicationConfiguration,
    InvalidSchemaVersionException,
    MandatoryConfigurationsException,
)
from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationInterface
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import AppType, KelvinAppConfiguration
from kelvin.sdk.lib.common.models.apps.ksdk_app_setup import AppCreationParametersObject
from kelvin.sdk.lib.common.models.factories.global_configurations_objects_factory import get_global_ksdk_configuration
from kelvin.sdk.lib.common.models.generic import KPath
from kelvin.sdk.lib.common.models.types import VersionStatus
from kelvin.sdk.lib.common.utils.general_utils import merge
from kelvin.sdk.lib.common.utils.logger_utils import logger
from kelvin.sdk.lib.common.utils.version_utils import assess_version_status


def generate_base_schema_template(app_creation_parameters_object: AppCreationParametersObject) -> dict:
    """
    Generate the base schema template.
    Attempt to retrieve the latest schema version and generate the default from it.

    :param app_creation_parameters_object: the app creation parameters object used to generate the default schema.

    :return: a dict containing the default app creation object.

    """
    latest_spec_version, latest_app_schema = get_latest_app_schema_version(overwrite_schema=True)

    def extend_with_default(validator_class) -> Any:  # type: ignore
        validate_properties = validator_class.VALIDATORS["properties"]

        def set_defaults(validator, properties, instance, schema):  # type: ignore
            for prop, sub_schema in properties.items():
                if "default" in sub_schema:
                    instance.setdefault(prop, sub_schema["default"])

            for error in validate_properties(validator, properties, instance, schema):
                yield error

        return validators.extend(validator_class, {"properties": set_defaults})

    app_name = app_creation_parameters_object.app_name
    app_type_obj: Dict[str, Any] = {"type": app_creation_parameters_object.app_type.value}

    if app_creation_parameters_object.app_type == AppType.kelvin:
        # 1 - Create the language block
        language_block = {"type": app_creation_parameters_object.kelvin_app_lang.value}
        language_block.update(app_creation_parameters_object.kelvin_app_lang.default_template(app_name=app_name))

        # 2 - Create the interface block
        app_interface: Optional[ApplicationInterface] = app_creation_parameters_object.kelvin_app_interface
        app_interface_value: Optional[str] = app_interface.value if app_interface else None
        app_interface_default_template: Dict[str, Any] = app_interface.default_template if app_interface else {}

        interface_block = {"type": app_interface_value, **app_interface_default_template}

        app_type_obj.update(
            {
                "kelvin": {
                    "images": {"base": "", "builder": ""},
                    "core": {
                        "version": "4.0.0",
                        "language": language_block,
                        "interface": interface_block,
                        "data_models": [],
                        "runtime": {
                            "type": "opcua",
                            "historize_inputs": False,
                            "historize_outputs": True,
                        },
                    },
                    "system_packages": [],
                },
            }
        )
        app_type_obj = merge({}, app_creation_parameters_object.default_template, app_type_obj)
    elif app_creation_parameters_object.app_type == AppType.bundle:
        app_type_obj = merge(
            {"bundle": {"images": {"base": "", "builder": ""}}},
            app_creation_parameters_object.default_template,
            app_type_obj,
        )
    else:
        app_type_obj.update(
            {
                "docker": {
                    "build": {
                        "context": ".",
                        "args": [],
                    }
                }
            }
        )

    creation_object = {
        "spec_version": latest_spec_version,
        "info": {
            "name": app_creation_parameters_object.app_name,
            "title": app_creation_parameters_object.app_name,
            "version": "1.0.0",
            "description": app_creation_parameters_object.app_description or app_creation_parameters_object.app_name,
        },
        "app": app_type_obj,
    }

    if latest_app_schema:
        extend_with_default(Draft7Validator)(latest_app_schema).validate(creation_object)

    _validate_schema(content=creation_object, schema=latest_app_schema)

    return creation_object


def validate_app_schema_from_app_config_file(
    app_config: Optional[Dict] = None, app_config_file_path: Optional[KPath] = None, overwrite_schema: bool = True
) -> bool:
    """
    When provided with an app configuration file, retrieve the schema for that version and validate it.

    :param app_config: the alternative app configuration to the app_config_file_path.
    :param app_config_file_path: the path to the app configuration.
    :param overwrite_schema: if specified, will overwrite the schema in the specified path.

    :return: indicates whether or not the schema complies with the provided spec.
    """
    app_config_content: dict = {}

    if app_config:
        app_config_content = app_config

    if not app_config_content and app_config_file_path:
        app_config_content = app_config_file_path.read_yaml()

    if not app_config_content:
        raise InvalidApplicationConfiguration()

    # Retrieve the current spec version, the minimum and latest values
    spec_version: Optional[str] = None
    try:
        spec_version = str(KelvinAppConfiguration(**app_config_content).spec_version)

        min_spec_version, latest_spec_version = get_min_and_latest_schema_versions_from_metadata()
        version_status = assess_version_status(
            current_version=spec_version, minimum_version=min_spec_version, latest_version=latest_spec_version
        )
        if version_status == VersionStatus.UNSUPPORTED:
            raise InvalidSchemaVersionException(
                min_version=min_spec_version, current_version=spec_version, latest_version=latest_spec_version
            )
    except InvalidSchemaVersionException:
        raise
    except Exception:
        logger.warning("No spec version defined. Proceeding with the latest schema version")

    schema_storage_path: KPath = KPath(SchemaManagerConfigs.schema_storage_path).expanduser().resolve()

    latest_schema = _get_and_persist_app_schema(
        schema_url=SchemaManagerConfigs.general_app_schema_url,
        schema_version=spec_version,
        schema_storage_path=schema_storage_path,
        overwrite_schema=overwrite_schema,
    )
    return _validate_schema(content=app_config_content, schema=latest_schema)


def get_latest_app_schema_version(overwrite_schema: bool = True) -> Tuple[str, Optional[dict]]:
    """
    Retrieve the latest app schema version and write to the schemas folder.

    :param overwrite_schema: indicates whether it should overwrite the existing schema.

    :return: a tuple containing both spec version and the corresponding schema.
    """
    schema_storage_path: KPath = KPath(SchemaManagerConfigs.schema_storage_path).expanduser().resolve()

    logger.info("Retrieving the latest schema version")

    _, latest_spec_version = get_min_and_latest_schema_versions_from_metadata()

    latest_schema = _get_and_persist_app_schema(
        schema_url=SchemaManagerConfigs.general_app_schema_url,
        schema_version=latest_spec_version,
        schema_storage_path=schema_storage_path,
        overwrite_schema=overwrite_schema,
    )
    return latest_spec_version, latest_schema


def get_min_and_latest_schema_versions_from_metadata() -> Tuple[str, str]:
    """
    Return the latest schema version from the metadata.

    :return: the tuple including both minimum and latest versions allowed from the schema.

    """

    global_ksdk_configuration = get_global_ksdk_configuration()
    url_metadata = global_ksdk_configuration.get_metadata_for_url()

    try:
        minimum_spec_version = url_metadata.kelvin_schema.minimum_spec_version
        latest_spec_version = url_metadata.kelvin_schema.latest_spec_version
    except Exception:
        raise MandatoryConfigurationsException(validation_error=None, message="No schema versions available")

    return minimum_spec_version, latest_spec_version


def _validate_schema(content: dict, schema: Optional[dict] = None, schema_path: Optional[KPath] = None) -> bool:
    """
    Validate a specific content against a schema.

    :param content: the content to validate.
    :param schema: the schema, as a dict, to validate the content against.
    :param schema_path: the path to the schema to validate the content against.

    :return: a bool indicating whether the provided content is valid.

    """
    try:
        schema_content = {}

        if schema:
            schema_content = schema

        if not schema_content and schema_path:
            logger.debug(f'Loading schema from "{schema_path}"')
            schema_content = json.loads(schema_path.read_text())

        if not schema_content:
            raise InvalidApplicationConfiguration(message="Please provide a valid schema")

        jsonschema.validate(instance=content, schema=schema_content)

        logger.debug("Provided content successfully validated against the schema")
        return True
    except Exception as exc:
        raise ContentDoesNotMatchSchemaException(message=str(exc))


def _get_and_persist_app_schema(
    schema_url: str, schema_version: Optional[str], schema_storage_path: KPath, overwrite_schema: bool = False
) -> Optional[dict]:
    """
    Attempt to retrieve the specified schema/version combination from the platform.

    :param schema_url: the url to retrieve the schema from.
    :param schema_version: the latest schema version.
    :param schema_storage_path: the path where the schema should be hosted.
    :param overwrite_schema: if specified, will overwrite the schema in the specified path.

    :return: the latest schema version of the platform.

    """
    specific_app_schema: Optional[dict] = None

    schema_path_aux = schema_storage_path / f"{schema_version}.json" if schema_version else schema_storage_path

    if not overwrite_schema and schema_path_aux and schema_path_aux.exists():
        logger.info(f"Valid schema available locally. Using cached version ({schema_path_aux})")
        specific_app_schema = schema_path_aux.read_json()

    if not specific_app_schema:
        specific_app_schema_response = requests.get(schema_url.format(version=schema_version))
        if specific_app_schema_response.status_code != 200:
            raise InvalidApplicationConfiguration(message=f'Invalid schema version "{schema_version}"')
        specific_app_schema = specific_app_schema_response.json()
        if schema_path_aux and specific_app_schema:
            schema_path_aux.write_json(content=specific_app_schema)

    return specific_app_schema
