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
from typing import Optional

import click
from click import Parameter
from pydantic import ValidationError

from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralMessages
from kelvin.sdk.lib.common.exceptions import AppException, AppNameIsInvalid
from kelvin.sdk.lib.common.models.apps.common import Name
from kelvin.sdk.lib.common.utils.general_utils import parse_pydantic_errors


def app_name_validator(value: Optional[Parameter]) -> Optional[Parameter]:
    try:
        check_if_app_name_is_valid(str(value))
    except Exception as exp:
        raise click.BadParameter(str(exp), param=value)
    return value


def check_if_app_name_is_valid(app_name: str) -> bool:
    """
    Verify whether the provided app name is valid (or contains a forbidden word combination).

    Raise an exception if the provided app name contains a forbidden keyword.

    :param app_name: the app name to be verified.

    :return: a boolean indicating whether the app name is valid.

    """
    try:
        invalid_keywords = ["python", "test"]
        if app_name in invalid_keywords:
            raise AppNameIsInvalid("\tPython-specific keywords are forbidden")
        Name.parse_obj(app_name)
    except ValidationError as exc:
        error_message = parse_pydantic_errors(validation_error=exc)
        raise AppException(GeneralMessages.invalid_app_name.format(reason=error_message))
    except AppNameIsInvalid as exc:
        raise AppException(GeneralMessages.invalid_app_name.format(reason=str(exc)))

    return True


def check_if_app_name_with_version_is_valid(app_name_with_version: str) -> bool:
    """
    Verify whether the provided app name is valid (or contains a forbidden word combination).

    Raise an exception if the provided app name contains a forbidden keyword.

    :param app_name_with_version: the app name to be verified. Includes the version

    :return: a boolean indicating whether the app name is valid.

    """

    _, app = app_name_with_version.split("/") if "/" in app_name_with_version else None, app_name_with_version

    split_values = app.split(":")

    if len(split_values) != 2:
        raise AppNameIsInvalid(GeneralMessages.invalid_app_name_with_version)
    app_name, app_version = split_values
    return check_if_app_name_is_valid(app_name=app_name)
