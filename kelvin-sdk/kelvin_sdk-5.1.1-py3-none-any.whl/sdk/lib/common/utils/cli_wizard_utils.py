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
from __future__ import annotations

from typing import Any, Callable, Optional

import click
from click import Choice

from kelvin.sdk.lib.common.configs.internal.cli_wizard_configs import AppCreationWizardConfigs
from kelvin.sdk.lib.common.models.apps.kelvin_app import ApplicationLanguage
from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import AppType
from kelvin.sdk.lib.common.models.apps.ksdk_app_setup import AppCreationParametersObject, CompatibilityTree
from kelvin.sdk.lib.common.models.generic import KSDKModel


class PromptStep(KSDKModel):
    key: str
    question: str
    result_type: Optional[Any]
    validator: Optional[Callable] = None


def start_app_creation_wizard() -> AppCreationParametersObject:
    """
    Creates the application creation object from a prompted wizard
    @return: an object with all the necessary variables for the creation of an application
    @rtype: AppCreationParametersObject
    """
    base_steps = [
        PromptStep(**AppCreationWizardConfigs.app_dir),
        PromptStep(**AppCreationWizardConfigs.app_name),
        PromptStep(**AppCreationWizardConfigs.app_description),
        PromptStep(**AppCreationWizardConfigs.app_type),
    ]
    result: dict = {}

    app_type: str = ""
    app_language: str = ""

    for item in base_steps:
        answer = click.prompt(item.question, type=item.result_type, value_proc=item.validator)
        result[item.key] = answer
        app_type = answer

    starting_tree = CompatibilityTree.tree

    if app_type and app_type not in ["bundle", "docker"]:
        starting_tree = starting_tree.get(AppType(app_type), {})
        app_lang_choices: list = [value.value_as_str for value in starting_tree.keys()]
        app_language = click.prompt("\n => Kelvin application language ", type=Choice(app_lang_choices))

    return_obj = AppCreationParametersObject(
        app_dir=result["app_dir"],
        app_name=result["app_name"],
        app_description=result["app_description"],
        app_type=AppType(app_type),
        kelvin_app_lang=ApplicationLanguage(app_language),
    )
    return return_obj
