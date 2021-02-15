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


from kelvin.sdk.client.error import APIError
from kelvin.sdk.lib.common.auth.auth_manager import (
    login_client_on_current_url,
    retrieve_error_message_from_api_exception,
)
from kelvin.sdk.lib.common.utils.display_utils import success_colored_message
from kelvin.sdk.lib.common.utils.logger_utils import logger


def acp_provision_script() -> bool:
    """
    Get the provisioning script to apply on an ACP.

    :return: a boolean indicating the end of the ACP provision script retrieval.

    """
    try:
        logger.info("Retrieving the ACP provision script..")

        client = login_client_on_current_url()

        provision_script = client.orchestration_provision.download_cluster_provision_script()
        script = provision_script.provision_script if provision_script.provision_script else ""
        script = success_colored_message(message=script)

        get_provision_script_warning: str = f"""\n
            # 1 - Prepare your ACP Host

               > Install Ubuntu 18.04 on your host.
               > The host must have at least 2GB of RAM, 10GB of Disk and a x86-64 Processor.


            # 2 - Install all necessary dependencies

               > To install and run the Kelvin Orchestration System, execute the following command on your host and 
                follow the prompted instructions:

                {script}

        """
        logger.info(get_provision_script_warning)

        return True

    except APIError as exc:
        error_message = retrieve_error_message_from_api_exception(api_error=exc)
        logger.error(f"Error retrieving the provision script: {error_message}")

    except Exception as exc:
        logger.exception(f"Error retrieving the provision script: {str(exc)}")

    return False
