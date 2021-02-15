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

from click import Choice

from kelvin.sdk.lib.common.models.apps.ksdk_app_configuration import AppType
from kelvin.sdk.lib.common.utils.application_utils import app_name_validator


class AppCreationWizardConfigs:
    app_dir: dict = {
        "key": "app_dir",
        "question": "\n => Application's directory ('.' for current directory) ",
        "result_type": str,
    }

    app_name: dict = {
        "key": "app_name",
        "question": "\n => Application name ",
        "result_type": str,
        "validator": app_name_validator,
    }

    app_description: dict = {
        "key": "app_description",
        "question": "\n => Application description ",
        "result_type": str,
    }

    app_type: dict = {
        "key": "app_type",
        "question": "\n => Application type ",
        "result_type": Choice(AppType.as_list()),
    }
