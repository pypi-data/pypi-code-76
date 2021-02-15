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

from typing import List, Optional, Sequence

from typeguard import typechecked

from kelvin.sdk.lib.common.utils.display_utils import DisplayObject


@typechecked
def secrets_create(secret_name: str, value: str) -> bool:
    """
    Create a secret on the platform.

    :param secret_name: The name of the secret to create.
    :param value: The value corresponding to the secret.

    :return: a boolean indicating whether or not the secret was successfully created on the Platform.

    """
    from kelvin.sdk.lib.common.api.secrets import secrets_create as _secrets_create

    return _secrets_create(secret_name=secret_name, value=value)


@typechecked
def secrets_list(query: Optional[str], should_display: bool = False) -> List[DisplayObject]:
    """
    List all the available secrets on the Platform.

    :param query: The query to filter the secrets by.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the secrets on the Platform.

    """
    from kelvin.sdk.lib.common.api.secrets import secrets_list as _secrets_list

    return _secrets_list(query=query, should_display=should_display)


@typechecked
def secrets_delete(secret_names: Sequence[str]) -> bool:
    """
    Delete secrets on the platform.

    :param secret_names: The names of the secrets to delete.

    :return: a boolean indicating whether or not the secret was successfully deleted on the Platform.

    """
    from kelvin.sdk.lib.common.api.secrets import secrets_delete as _secrets_delete

    return _secrets_delete(secret_names=secret_names)
