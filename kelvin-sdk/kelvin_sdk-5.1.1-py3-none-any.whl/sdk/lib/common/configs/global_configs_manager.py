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

from typing import List, Tuple

from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.models.factories.global_configurations_objects_factory import get_global_ksdk_configuration
from kelvin.sdk.lib.common.utils.display_utils import DisplayObject, display_data_entries, success_colored_message
from kelvin.sdk.lib.common.utils.general_utils import get_url_encoded_string
from kelvin.sdk.lib.common.utils.logger_utils import logger
from kelvin.sdk.lib.common.utils.version_utils import color_formats


def global_configurations_list(should_display: bool = False) -> List[DisplayObject]:
    """
    List all available configurations for KSDK

    :param should_display: specifies whether or not the display should output data.

    :return: the list of all available configurations and their current details.

    """
    try:
        global_ksdk_configuration = get_global_ksdk_configuration()
        descriptions = global_ksdk_configuration.kelvin_sdk.configurations.descriptions
        private_fields = global_ksdk_configuration.kelvin_sdk.configurations.private_fields

        data = [v for k, v in descriptions.items() if k not in private_fields]

        display_obj = display_data_entries(
            data=data,
            header_names=["Variable", "Description", "Current Value"],
            attributes=["env", "description", "current_value"],
            table_title=GeneralConfigs.table_title.format(title="Environment Variables"),
            should_display=should_display,
        )
        set_unset_command = success_colored_message("kelvin configuration set/unset")
        logger.info(f"See {set_unset_command} for more details on how to configure this tool.")
        return [display_obj]

    except Exception as exc:
        logger.exception(f"Error retrieving environment variable configurations: {str(exc)}")
        return []


def global_configurations_set(configuration: Tuple) -> bool:
    """
    Set the specified configuration on the platform system

    :param configuration: the configuration tuple that includes both the configuration and respective value.

    :return: a boolean indicating the configuration was successfully set.

    """
    try:
        global_ksdk_configuration = get_global_ksdk_configuration()
        return global_ksdk_configuration.set_configuration(config=configuration[0], value=configuration[1])
    except Exception as exc:
        logger.exception(f"Error setting configuration variable: {str(exc)}")
        return False


def global_configurations_unset(configuration: str) -> bool:
    """
    Unset the specified configuration from the platform system

    :param configuration: the configuration to unset.

    :return: a boolean indicating the configuration was successfully set.

    """
    try:
        global_ksdk_configuration = get_global_ksdk_configuration()
        return global_ksdk_configuration.unset_configuration(config=configuration)
    except Exception as exc:
        logger.exception(f"Error un-setting configuration variable: {str(exc)}")
        return False


def encode_string(value: str) -> str:
    """
    Return the url-encoded version of the provided string.

    Parameters
    ----------
    value : str
        the value to be url-encoded.

    Returns
    -------
    str
        the url-encoded value.

    """
    url_encoded_value = get_url_encoded_string(original_string=value)
    encode_display: str = f"""

        The encoded value is:

            {url_encoded_value}
    """
    logger.info(encode_display)
    return url_encoded_value


def pip_configure() -> bool:
    """
    A setup utility that shows how a pip configuration can be set

    """
    pip_configure_guide: str = """

        In order to access python packages that are hosted in private pypi repositories, credentials must be provided.

        Kelvin-sdk currently supports the following methods:
            1 - Export an environment variable.
            2 - Setup the official pip configuration file: pip.conf (unix) / pip.ini (windows)

        {yellow}
        Warning: PyPi credentials must be url-encoded to prevent string termination issues.

        Please refer to `kelvin configuration pip encode` for more details.
        {reset}

        # 1 - Environment variable:
            For unix-based systems (e.g. MacOS, Ubuntu, etc) simply export it on the running shell.
            e.g:

            {green}
            $ export PIP_EXTRA_INDEX_URL="https://user:encoded_pass@nexus.kelvininc.com/repository/pypi-kelvin/simple"
            {reset}

        # 2 - Official pip configuration file:
            The pip configuration file can be consulted with following command.
            If it does not exist, create it:
                {green}
                $ pip3 config -v list

                tip: on MacOS/Linux, it is usually hosted under '~/.config/pip/pip.conf'
                {reset}
            Edit the yielded file and set your credentials.
            e.g:
            {green}

            [global]
            extra-index-url =
                https://user:encoded_pass@nexus.kelvininc.com/repository/pypi-kelvin/simple
            {reset}

    """
    logger.info(pip_configure_guide.format_map(color_formats))
    return True
