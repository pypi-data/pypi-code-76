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

from typing import List, Optional, Sequence, cast

from kelvin.sdk.client.error import APIError
from kelvin.sdk.client.model.requests import SecretCreate
from kelvin.sdk.lib.common.auth.auth_manager import (
    login_client_on_current_url,
    retrieve_error_message_from_api_exception,
)
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.utils.display_utils import DisplayObject, display_data_entries, display_yes_or_no_question
from kelvin.sdk.lib.common.utils.logger_utils import logger


def secrets_create(secret_name: str, value: str) -> bool:
    """
    Create a secret on the Platform.

    :param secret_name: The name of the ACP to filter the search.
    :param value: The source of data.

    :return: a boolean indicating whether or not the secret was successfully created on the Platform.

    """
    try:
        logger.info(f'Creating secret "{secret_name}" on the platform')

        client = login_client_on_current_url()

        secret_create_request = SecretCreate(name=secret_name, value=value)

        client.secret.create_secret(data=secret_create_request)

        logger.relevant(f'Secret "{secret_name}" successfully created on the platform')

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error creating secret: {error_message}")

    except Exception as exc:
        logger.exception(f"Error creating secret: {str(exc)}")

    return False


def secrets_list(query: Optional[str], should_display: bool = False) -> List[DisplayObject]:
    """
    List all the available secrets on the Platform.

    :param query: query to filter secrets for.
    :param should_display: specifies whether or not the display should output data.

    :return: a list of DisplayObject instances that wrap up the secrets on the Platform.

    """
    try:
        logger.info("Retrieving platform secrets..")

        client = login_client_on_current_url()

        yielded_secrets = cast(List, client.secret.list_secret(search=query)) or []

        display_data = display_data_entries(
            data=yielded_secrets,
            header_names=["Secret name"],
            attributes=["name"],
            table_title=GeneralConfigs.table_title.format(title="Secrets"),
            should_display=False,
            no_data_message="No secrets available",
        )

        if should_display and display_data:
            logger.info(f"{display_data.tabulated_data}")

        return [display_data]

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error retrieving secrets: {error_message}")

    except Exception as exc:
        logger.exception(f"Error retrieving secrets: {str(exc)}")

    return []


def secrets_delete(secret_names: Sequence[str]) -> bool:
    """
    Delete secrets on the Platform.

    :param secret_names: The names of the secrets to delete.

    :return: a boolean indicating whether or not the secrets were successfully deleted on the Platform.

    """
    result = True

    secrets_description = ", ".join(secret_names)
    logger.info(f'Deleting secret(s) "{secrets_description}" from the platform')

    prompt_question = f'This operation will delete the secret(s) "{secrets_description}" from the platform.'
    confirm = display_yes_or_no_question(question=prompt_question)

    if confirm:
        client = login_client_on_current_url()

        for secret_name in secret_names:
            try:
                client.secret.delete_secret(secret_name=secret_name)
                logger.relevant(f'Secret "{secret_name}" successfully deleted from the platform')

            except APIError as exc:
                error_message = retrieve_error_message_from_api_exception(api_error=exc)
                logger.error(f"Error deleting secret: {error_message}")
                result = False

            except Exception as exc:
                logger.exception(f"Error deleting secret: {str(exc)}")
                result = False

    return result
