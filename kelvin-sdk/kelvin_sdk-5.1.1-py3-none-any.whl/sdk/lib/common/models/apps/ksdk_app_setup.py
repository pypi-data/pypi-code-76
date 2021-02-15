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

from stat import S_IEXEC
from typing import Any, Dict, List, Mapping, Optional

from jinja2 import Template
from pydantic import validator

from kelvin.sdk.lib.common.exceptions import AppNameIsInvalid
from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationFlavour, ApplicationInterface, ApplicationLanguage
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import AppType, KelvinAppConfiguration
from kelvin.sdk.lib.common.models.generic import KPath, KSDKModel
from kelvin.sdk.lib.common.models.legacy.ksdk_app_configuration import LegacyAppGlobalConfiguration


class TemplateFile(KSDKModel):
    name: str
    content: Template
    options: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True


class File(KSDKModel):
    file: KPath
    content: str
    executable: bool = False

    def create(self) -> bool:
        self.file.write_content(self.content)
        if self.executable:
            self.file.chmod(self.file.stat().st_mode | S_IEXEC)
        return True

    @validator("content")
    def content_exists(cls, v: str) -> Any:  # noqa
        return v if v is not None else ""


class Directory(KSDKModel):
    directory: KPath
    files: List[File] = []

    def create(self) -> bool:
        self.directory.create_dir()
        return True

    def delete(self) -> bool:
        import shutil

        shutil.rmtree(self.directory, ignore_errors=True)
        return True


# Legacy
class LegacyBaseBuildingObject(KSDKModel):
    custom_app: bool = False
    build_for_data_model_compilation: bool = False
    build_for_upload: bool = False
    dockerfile_path: KPath
    docker_build_context_path: KPath
    # base docker image configurations
    base_data_model_builder_image: Optional[str]
    base_image: Optional[str]
    # docker image names and labels
    docker_image_name: str
    docker_image_version: str
    docker_image_labels: dict
    build_args: Optional[Dict[str, str]] = None

    @property
    def full_docker_image_name(self) -> str:
        return f"{self.docker_image_name}:{self.docker_image_version}"


class LegacyAppBuildingObjectLegacy(LegacyBaseBuildingObject):
    app_config_file_path: KPath
    app_config_model: LegacyAppGlobalConfiguration
    app_dir_path: KPath
    app_build_dir_path: KPath
    app_datamodel_dir_path: KPath
    requirements_file: Optional[str]
    system_packages_file_path: Optional[KPath]


# App creation
class AppCreationObject(KSDKModel):
    app_root_dir: Directory
    app_dir: Optional[Directory]
    build_dir: Optional[Directory]
    data_dir: Optional[Directory]
    datamodel_dir: Optional[Directory]
    docs_dir: Optional[Directory]
    shared_dir: Optional[Directory]
    tests_dir: Optional[Directory]

    def fundamental_dirs_and_files(self) -> List[Directory]:
        return [self.app_root_dir]

    def optional_dirs_and_files(self) -> List[Directory]:
        return [
            directory
            for directory in [
                self.app_dir,
                self.build_dir,
                self.data_dir,
                self.datamodel_dir,
                self.tests_dir,
                self.docs_dir,
                self.shared_dir,
                self.tests_dir,
            ]
            if directory
        ]


class AppCreationParametersObject(KSDKModel):
    app_dir: str
    app_name: str
    app_description: str
    app_type: AppType
    kelvin_app_lang: ApplicationLanguage = ApplicationLanguage.python
    create_env: bool = False

    @property
    def kelvin_app_interface(self) -> Optional[ApplicationInterface]:
        if self.kelvin_app_lang:
            if self.kelvin_app_lang == ApplicationLanguage.python:
                return ApplicationInterface.client
            elif self.kelvin_app_lang == ApplicationLanguage.cpp:
                return ApplicationInterface.data
        return None

    @property
    def kelvin_app_flavour(self) -> Optional[ApplicationFlavour]:
        if self.kelvin_app_lang:
            if self.kelvin_app_lang == ApplicationLanguage.python:
                return ApplicationFlavour.kelvin_app
            elif self.kelvin_app_lang == ApplicationLanguage.cpp:
                return ApplicationFlavour.core
        return None

    @validator("app_name", pre=True)
    def single_app_name(cls, value: Any) -> str:  # noqa
        if value:
            if isinstance(value, str):
                return value
            elif isinstance(value, tuple):
                return value[0]
        raise AppNameIsInvalid()

    @property
    def default_template(self) -> Mapping[str, Any]:

        value: Dict[str, Any] = {}

        if (
            self.app_type == AppType.kelvin
            and self.kelvin_app_interface == ApplicationInterface.client
            and self.kelvin_app_lang == ApplicationLanguage.python
        ):
            value.update(
                {
                    self.app_type.name: {
                        "core": {
                            "interface": {
                                self.kelvin_app_interface.name: {
                                    "executable": "run_app",
                                    "args": [],
                                    "spawn": True,
                                }
                            }
                        }
                    }
                }
            )
        elif self.app_type == AppType.bundle:
            value.update(
                {
                    self.app_type.name: {
                        "pipelines": [
                            {"name": "my-app", "version": "1.0.0"},
                        ]
                    }
                }
            )

        return value

    @property
    def assess_parameters_validity(
        self,
    ) -> bool:
        app_type_str = self.app_type.value_as_str
        app_lang_str = self.kelvin_app_lang.value_as_str

        # For docker and bundle types (when the subtree below the app_type is none)
        if self.app_type in [AppType.kelvin]:
            starting_tree: dict = CompatibilityTree.tree.get(self.app_type, {})
            if self.kelvin_app_lang not in starting_tree.keys():
                raise ValueError(f'Application type "{app_type_str}" does not support language "{app_lang_str}"')

        return True


# App building
class BaseAppBuildingObject(KSDKModel):
    fresh_build: bool = False
    build_for_upload: bool = False
    app_config_file_path: KPath
    app_config_raw: Dict
    app_config_model: KelvinAppConfiguration
    app_dir_path: KPath
    app_build_dir_path: KPath
    docker_image_labels: dict
    docker_image_name: str

    @property
    def full_docker_image_name(self) -> str:
        return f"{self.app_config_model.info.name}:{self.app_config_model.info.version}"


class KelvinAppBuildingObject(BaseAppBuildingObject):
    dockerfile_path: KPath
    docker_build_context_path: KPath
    # base docker image configurations
    base_image: str
    base_data_model_builder_image: str
    # docker image names and labels
    docker_image_version: str
    # external arguments - pypi credentials
    build_args: Optional[Dict[str, str]] = None
    # app directories
    app_datamodel_dir_path: Optional[KPath] = None
    # utility flags
    build_for_data_model_compilation: bool = False
    upload_datamodels: bool = False


class BundleAppBuildingObject(KelvinAppBuildingObject):
    system_packages: List[str] = []
    python_paths: List[str] = []


class DockerAppBuildingObject(BaseAppBuildingObject):
    pass


# Generic
class ApplicationName:
    name: str
    version: Optional[str]

    def __init__(self, name: str, version: Optional[str] = None) -> None:
        self.name = name
        self.version = version
        if ":" in name:
            self.name, self.version = name.split(":")

    @property
    def full_name(self) -> str:
        """
        Get the "dockerized" full name of an application from its variables.
        Return the app name if no version is specified.

        :return: a string.
        """
        return f"{self.name}:{self.version}" if self.version else self.name

    def dict(self) -> dict:
        """
        Return itself as a dict.
        """
        result = self.__dict__
        result["full_name"] = self.full_name
        return result


class CompatibilityTree:
    tree: dict = {
        AppType.kelvin: {
            ApplicationLanguage.python: {
                ApplicationInterface.client: {
                    ApplicationFlavour.kelvin_app: {},
                },
            },
            ApplicationLanguage.cpp: {
                ApplicationInterface.data: {
                    ApplicationFlavour.core: {},
                },
            },
        },
        AppType.bundle: {},
        AppType.docker: {},
    }
