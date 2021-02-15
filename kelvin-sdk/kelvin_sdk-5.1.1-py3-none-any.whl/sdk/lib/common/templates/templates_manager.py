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

from types import MappingProxyType
from typing import Dict, List, Optional

from jinja2 import Environment, PackageLoader, Template

from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationFlavour, ApplicationInterface, ApplicationLanguage
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import AppType
from kelvin.sdk.lib.common.models.apps.ksdk_app_setup import TemplateFile
from kelvin.sdk.lib.common.models.types import EmbeddedFiles, FileType


def get_app_templates(
    app_type: AppType,
    file_type: FileType,
    kelvin_app_lang: Optional[ApplicationLanguage] = None,
    kelvin_app_interface: Optional[ApplicationInterface] = None,
    kelvin_app_flavour: Optional[ApplicationFlavour] = None,
) -> List[TemplateFile]:
    """
    When provided with a programming language and file type, retrieve all of the respective templates.

    :param app_type: the app type of the desired templates.
    :param kelvin_app_lang: the programming app language of the desired templates.
    :param kelvin_app_interface: the programming app language of the desired templates.
    :param kelvin_app_flavour: the app style of the desired templates.
    :param file_type: the type of templates to retrieve (either app templates or configuration templates).

    :return: a list of TemplateFiles.

    """

    if app_type == AppType.kelvin:
        templates = (
            _app_templates.get(app_type, {})
            .get(kelvin_app_lang, {})
            .get(kelvin_app_interface, {})
            .get(kelvin_app_flavour, {})
            .get(file_type, [])
        )
        defaults: List[Dict[str, str]] = (
            _app_templates.get(app_type, {})
            .get(kelvin_app_lang, {})
            .get(kelvin_app_interface, {})
            .get(None, {})
            .get(file_type, [])
        )
        template_names = {x["name"] for x in templates}
        templates += [x for x in defaults if x["name"] not in template_names]
    else:
        templates = _app_templates.get(app_type, {}).get(file_type, [])

    return [
        TemplateFile(
            name=item.get("name"),
            content=_retrieve_template(template_name=item.get("content", "")),
            options=item.get("options", {}),
        )
        for item in templates
    ]


def get_embedded_file(embedded_file: EmbeddedFiles) -> Template:
    """
    When provided with an embedded app type and file type, retrieve all of the respective templates.

    :param embedded_file: the type of the embedded app to retrieve the templates from.

    :return: a list of TemplateFiles.

    """
    template = _embedded_files.get(embedded_file, {})

    return _retrieve_template(template_name=template)


def _retrieve_template(template_name: str) -> Template:
    """
    Retrieve the Jinja2 Template with the specified template name (path).

    :param template_name: the name of the template to retrieve.

    :return: a Jinja2 template.

    """
    templates_package_loader = PackageLoader(package_name="kelvin.sdk.lib", package_path="common/templates")
    templates_environment = Environment(loader=templates_package_loader, trim_blocks=True, autoescape=True)
    return templates_environment.get_template(name=template_name)


_app_templates: MappingProxyType = MappingProxyType(
    {
        AppType.kelvin: {
            ApplicationLanguage.python: {
                ApplicationInterface.client: {
                    None: {
                        FileType.APP: [],
                        FileType.CONFIGURATION: [
                            {
                                "name": GeneralConfigs.default_python_setup_file,
                                "content": "apps/kelvin/python/python_app_setup_file.jinja2",
                            },
                            {
                                "name": GeneralConfigs.default_requirements_file,
                                "content": "apps/kelvin/python/python_app_requirements_file.jinja2",
                            },
                            {
                                "name": GeneralConfigs.default_git_ignore_file,
                                "content": "apps/kelvin/python/python_app_gitignore_file.jinja2",
                            },
                            {
                                "name": GeneralConfigs.default_docker_ignore_file,
                                "content": "files/default_dockerignore.jinja2",
                            },
                        ],
                        FileType.BUILD: [],
                        FileType.DATA: [],
                        FileType.DATAMODEL: [
                            {
                                "name": GeneralConfigs.default_git_keep_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                        FileType.DOCS: [
                            {
                                "name": GeneralConfigs.default_git_keep_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                        FileType.SHARED: [
                            {
                                "name": GeneralConfigs.default_git_keep_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                        FileType.TESTS: [
                            {
                                "name": GeneralConfigs.default_python_init_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                    },
                    ApplicationFlavour.kelvin_app: {
                        FileType.APP: [
                            {
                                "name": GeneralConfigs.default_python_init_file,
                                "content": "apps/kelvin/python/python_app_init_file.jinja2",
                            },
                            {
                                "name": "{app_file_system_name}{app_lang_extension}",
                                "content": "apps/kelvin/python/client/kelvin_app/python_kelvin_app_file.jinja2",
                            },
                        ],
                        FileType.DATA: [
                            {
                                "name": GeneralConfigs.default_git_keep_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                        FileType.TESTS: [
                            {
                                "name": GeneralConfigs.default_python_test_file,
                                "content": "apps/kelvin/python/client/kelvin_app/python_kelvin_app_tests_file.jinja2",
                            },
                        ],
                    },
                },
            },
            ApplicationLanguage.cpp: {
                ApplicationInterface.data: {
                    ApplicationFlavour.core: {
                        FileType.APP: [
                            {
                                "name": "{app_file_system_name}{app_lang_extension}",
                                "content": "apps/kelvin/cpp/data/core/cpp_core_app_implementation.jinja2",
                            },
                            {
                                "name": "{app_file_system_name}{cpp_app_header_extension}",
                                "content": "apps/kelvin/cpp/data/core/cpp_core_app_header.jinja2",
                            },
                            {
                                "name": GeneralConfigs.default_cmakelists_file,
                                "content": "apps/kelvin/cpp/cpp_app_make_build.jinja2",
                            },
                        ],
                        FileType.CONFIGURATION: [
                            {
                                "name": GeneralConfigs.default_git_ignore_file,
                                "content": "apps/kelvin/cpp/cpp_app_gitignore.jinja2",
                            },
                            {
                                "name": GeneralConfigs.default_docker_ignore_file,
                                "content": "files/default_dockerignore.jinja2",
                            },
                        ],
                        FileType.BUILD: [],
                        FileType.DATA: [
                            {
                                "name": GeneralConfigs.default_git_keep_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                        FileType.DATAMODEL: [
                            {
                                "name": GeneralConfigs.default_git_keep_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                        FileType.DOCS: [
                            {
                                "name": GeneralConfigs.default_git_keep_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                        FileType.SHARED: [
                            {
                                "name": GeneralConfigs.default_git_keep_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                        FileType.TESTS: [
                            {
                                "name": GeneralConfigs.default_git_keep_file,
                                "content": "files/default_empty_file.jinja2",
                            },
                        ],
                    },
                },
            },
        },
        AppType.bundle: {
            FileType.CONFIGURATION: [
                {
                    "name": GeneralConfigs.default_docker_ignore_file,
                    "content": "files/default_dockerignore.jinja2",
                },
                {
                    "name": GeneralConfigs.default_git_ignore_file,
                    "content": "apps/kelvin/python/python_app_gitignore_file.jinja2",
                },
            ],
        },
        AppType.docker: {
            FileType.CONFIGURATION: [
                {
                    "name": GeneralConfigs.default_docker_ignore_file,
                    "content": "files/default_dockerignore.jinja2",
                },
                {
                    "name": GeneralConfigs.default_dockerfile,
                    "content": "files/default_empty_file.jinja2",
                },
            ],
        },
    },
)

_embedded_files: MappingProxyType = MappingProxyType(
    {
        EmbeddedFiles.EMPTY_FILE: "files/default_empty_file.jinja2",
        EmbeddedFiles.DOCKERIGNORE: "files/default_dockerignore.jinja2",
        EmbeddedFiles.PYTHON_APP_GITIGNORE: "apps/kelvin/python/python_app_gitignore_file.jinja2",
        EmbeddedFiles.PYTHON_APP_DOCKERFILE: "docker/python_app_dockerfile.jinja2",
        EmbeddedFiles.BUNDLE_APP_DOCKERFILE: "docker/bundle_app_dockerfile.jinja2",
        EmbeddedFiles.CPP_APP_DOCKERFILE: "docker/cpp_app_dockerfile.jinja2",
        EmbeddedFiles.DEFAULT_DATAMODEL_TEMPLATE: "files/default_datamodel_icd.jinja2",
    }
)
