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
import sys
import time
from getpass import getpass
from typing import List, Optional, Sequence

from kelvin.sdk.client import Client
from kelvin.sdk.client.error import APIError
from kelvin.sdk.lib.common.configs.internal.auth_manager_configs import AuthManagerConfigs
from kelvin.sdk.lib.common.configs.internal.general_configs import GeneralConfigs
from kelvin.sdk.lib.common.exceptions import KSDKException
from kelvin.sdk.lib.common.models.factories.global_configurations_objects_factory import get_global_ksdk_configuration
from kelvin.sdk.lib.common.utils.display_utils import display_yes_or_no_question
from kelvin.sdk.lib.common.utils.logger_utils import logger

from ..configs.internal.schema_manager_configs import SchemaManagerConfigs
from ..models.generic import KPath
from ..models.ksdk_global_configuration import KelvinSDKGlobalConfiguration


# 1 - Login
def login_on_url(
    url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    totp: Optional[str] = None,
    reset: bool = False,
) -> bool:
    """
    Logs the user into the provided url.

    :param url: the url to log on.
    :param username: the username of the client site.
    :param password: the password corresponding to the username.
    :param totp: the totp authentication_token.
    :param reset: if set to True, will clear the existing configuration prior to the new session.

    :return: a boolean indicating whether the user was successfully logged in.

    """
    successfully_logged_on_client = False
    try:
        if reset:
            reset_configurations()

        url = url or input("Platform: ")
        username_missing = username is None and password is not None
        password_missing = username is not None and password is None
        empty_credentials = username is None and password is None

        if username_missing or password_missing:
            ksdk_auth_incomplete_credentials: str = """Incomplete credentials. \n
                Either provide both credentials or follow the prompt."""
            raise KSDKException(ksdk_auth_incomplete_credentials)

        if empty_credentials:
            username = input("Enter your username: ")
            password = getpass(prompt="Enter your password: ")
            totp_prompt: str = "Enter 2 Factor Authentication (2FA) one-time password (blank if not required): "
            totp = getpass(totp_prompt) or None

        # 1 - Ensure the ksdk configuration file exists before proceeding
        ksdk_configuration = get_global_ksdk_configuration()

        if not username or not password:
            raise KSDKException(message="Please provide a valid set of credentials")

        url = url or ksdk_configuration.kelvin_sdk.current_url
        if not url:
            raise KSDKException(message="No session currently available. Please provide a valid url argument")

        # 2 - Save the client configuration to the client configuration
        client = _fresh_client_login_for_url(
            url=url,
            ksdk_configuration=ksdk_configuration,
            username=username,
            password=password,
            totp=totp,
        )

        successfully_logged_on_client = client is not None

        if successfully_logged_on_client:
            logger.relevant(f'Successfully logged on "{url}"')

    except Exception as exc:
        ksdk_auth_failure: str = f"""Error authenticating: {str(exc)} \n
            Consider invalidating authentication cache with `kelvin auth login --reset`.
        """
        logger.exception(ksdk_auth_failure)

    return successfully_logged_on_client


def login_client_on_current_url(
    ksdk_configuration: KelvinSDKGlobalConfiguration = None,
    login: bool = True,
    verbose: bool = True,
    force_metadata: bool = False,
) -> Client:
    """
    Performs a fresh login on the current url, retrieving the instantiated KelvinClient object.

    :param ksdk_configuration: the ksdk configuration object that contains all session data to be handled.
    :param login: hints the Kelvin SDK Client object it should perform a login.
    :param verbose: indicates whether the Kelvin SDK Client object should display all verbose logs.
    :param force_metadata: indicates whether the Kelvin SDK Client object should force fetch metadata.

    :return: a ready-to-use KelvinClient object.

    """
    ksdk_configuration = ksdk_configuration or get_global_ksdk_configuration()
    try:
        current_url = ksdk_configuration.kelvin_sdk.current_url
        current_user = ksdk_configuration.kelvin_sdk.current_user
        current_company_metadata = ksdk_configuration.get_metadata_for_url()
        kwargs = {"metadata": None} if force_metadata else {}
        client = Client.from_file(
            ksdk_configuration.kelvin_sdk_client_config_file_path,
            site=current_url,
            url=current_url,
            username=current_user,
            realm_name=current_company_metadata.authentication.realm,
            login=login,
            verbose=verbose,
            timeout=AuthManagerConfigs.kelvin_client_timeout_thresholds,
            **kwargs,  # type: ignore
        )
        return client
    except Exception:
        raise ConnectionError(AuthManagerConfigs.invalid_session_message)


# 2 - Logout
def logout_from_all_sessions(ignore_destructive_warning: bool = False) -> bool:
    """
    Logs off the client all currently stored sessions.

    :param ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    :return: a boolean indicating whether the user was successfully logged out.

    """
    logged_out = False
    try:
        if not ignore_destructive_warning:
            ignore_destructive_warning = display_yes_or_no_question("")

        if ignore_destructive_warning:
            ksdk_configuration = get_global_ksdk_configuration()
            if ksdk_configuration:
                logged_out = bool(ksdk_configuration.reset_ksdk_configuration().commit_ksdk_configuration())
            if not logged_out:
                raise ConnectionError(AuthManagerConfigs.invalid_session_message)
            logger.relevant("Successfully logged off client from all sessions")

    except Exception as exc:
        logger.error(str(exc))

    return logged_out


# 3 - Force Refresh metadata
def refresh_metadata(
    ksdk_configuration: Optional[KelvinSDKGlobalConfiguration] = None,
) -> Optional[KelvinSDKGlobalConfiguration]:
    """
    A simple wrapper method to refresh metadata on request.

    :param ksdk_configuration: the ksdk configuration object that contains all session data to be handled.

    :return: a boolean indicating whether or not the metadata was successfully refreshed.
    """
    try:
        # 1 - Get the current configuration
        ksdk_configuration = ksdk_configuration or get_global_ksdk_configuration()
        # 2 - Assess the last timestamp
        try:
            last_metadata_retrieval = int(ksdk_configuration.kelvin_sdk.last_metadata_refresh)
        except TypeError:
            last_metadata_retrieval = 0
        # 3 - check the difference
        time_difference = time.time() - last_metadata_retrieval
        twelve_hours_cap_is_crossed = time_difference >= 12 * 3600
        # 4 - If it crosses the 12h threshold, force refresh
        if twelve_hours_cap_is_crossed:
            logger.info("Refreshing metadata..")
            login_client_on_current_url(force_metadata=True)
            url_metadata = ksdk_configuration.get_metadata_for_url(url=ksdk_configuration.kelvin_sdk.current_url)
            ksdk_configuration.kelvin_sdk.last_metadata_refresh = time.time()
            ksdk_configuration.kelvin_sdk.ksdk_minimum_version = url_metadata.sdk.ksdk_minimum_version
            ksdk_configuration.kelvin_sdk.ksdk_latest_version = url_metadata.sdk.ksdk_latest_version
            return ksdk_configuration.commit_ksdk_configuration()
    except ConnectionError:
        logger.debug("Could not retrieve metadata. Proceeding regardless..")
    return None


def reset_configurations() -> bool:
    """
    Resets all KSDK configurations

    :return: a symbolic flag indicating the configuration was reset.

    """
    try:
        logger.info("Resetting KSDK configurations..")
        # 1 - get the variables
        files_to_reset: List[KPath] = [
            KPath(GeneralConfigs.default_ksdk_configuration_file).expanduser().resolve(),
            KPath(GeneralConfigs.default_kelvin_sdk_client_configuration_file).expanduser().resolve(),
            KPath(SchemaManagerConfigs.schema_storage_path).expanduser().resolve(),
        ]
        # 2 - delete all files
        for item in files_to_reset:
            if item.exists():
                if item.is_dir():
                    item.delete_dir()
                else:
                    item.unlink()
        logger.info("KSDK configurations successfully reset")
        return True
    except Exception as exc:
        logger.exception(f"Error resetting KSDK configurations: {str(exc)}")
        return False


def authentication_token(full: bool, margin: float = 10.0) -> bool:
    """
    Obtain an authentication authentication_token from the API.

    :param full: return the full authentication_token.
    :param margin: minimum time to expiry.

    :return: a boolean indicating whether the authentication_token was successfully obtained.
    """

    margin = max(margin, 0.0)
    force = margin <= 0.0

    try:
        client = login_client_on_current_url(login=False, verbose=False)
        client.login(force=force, margin=margin)
    except Exception as exc:
        logger.error(str(exc))
        return False

    if full:
        json.dump(client.token, sys.stdout, indent=2)
    else:
        sys.stdout.write(client.token["access_token"])

    return True


def launch_ipython_client(args: Sequence[str]) -> None:
    """
    Launch an interactive IPython console with the pre-logged, already-built (kelvin.sdk.client) client.

    """
    import IPython
    from traitlets.config import Config

    if args:
        sys.argv[:] = args
        if args[0] == "-":
            args = ("", *args[1:])
    else:
        sys.argv[:] = [""]

    config = Config()
    config.TerminalInteractiveShell.banner1 = ""
    config.TerminalInteractiveShell.banner2 = """
        **************** Kelvin SDK Client *****************
        ************ Platform API access loaded ************
        *** type 'client' and tab to autocomplete ***
    """

    try:
        user_ns = {"client": login_client_on_current_url()}
        sys.exit(IPython.start_ipython(["--", *args], user_ns=user_ns, config=config))
    except Exception as exc:
        logger.exception(str(exc))


# 4 - Utils
def _fresh_client_login_for_url(
    url: str,
    username: str,
    password: str,
    totp: Optional[str],
    ksdk_configuration: KelvinSDKGlobalConfiguration,
) -> Client:
    """
    Setup a fresh login, writing the required configurations to target ksdk configuration file path.

    Sets up the kelvin API client configuration to allow api interaction.
    Sets up the kelvin sdk configuration to allow the storage of specific ksdk variables.

    :param url: the url to login to.
    :param username: the username of the client site.
    :param password: the password corresponding to the username.
    :param totp: the TOTP corresponding to the username.
    :param ksdk_configuration: the object that contains global ksdk configurations.

    :return: a ready-to-use KelvinClient object.

    """
    logger.info(f'Attempting to log on "{url}"')

    try:
        # Prepare metadata retrieval
        client = Client.from_file(
            ksdk_configuration.kelvin_sdk_client_config_file_path,
            site=url,
            username=username,
            create=True,
            verbose=True,
            timeout=AuthManagerConfigs.kelvin_client_timeout_thresholds,
        )
        client.login(password=password, totp=totp, force=True)
        # Retrieve the versions and set them once the client access is done
        url_metadata = ksdk_configuration.get_metadata_for_url(url=url)
        ksdk_configuration.kelvin_sdk.last_metadata_refresh = time.time()
        ksdk_configuration.kelvin_sdk.current_url = url
        ksdk_configuration.kelvin_sdk.current_user = username
        ksdk_configuration.kelvin_sdk.ksdk_minimum_version = url_metadata.sdk.ksdk_minimum_version
        ksdk_configuration.kelvin_sdk.ksdk_latest_version = url_metadata.sdk.ksdk_latest_version
        ksdk_configuration.commit_ksdk_configuration()
        return client
    except Exception as inner_exception:
        try:
            ksdk_configuration.reset_ksdk_configuration().commit_ksdk_configuration()
        except Exception:
            raise inner_exception
        raise inner_exception


def retrieve_error_message_from_api_exception(api_error: APIError) -> str:
    """
    Returns the 'pretty' error message from the APIError.

    :param api_error: The exception yielded by the service call.

    :return: a string containing the error message of the APIError.

    """
    try:
        message: str = ""
        api_errors = api_error.errors

        for error in api_errors:
            if error.http_status_code and error.http_status_code == 403:
                no_permission_error_message: str = """\n
                    You don’t have the required permissions to execute this command.\n
                    Please contact your system administrator. \n
                """
                return no_permission_error_message
            error_message = error.message
            if isinstance(error_message, list):
                converted_error_message = " ".join(item for item in error_message)
            else:
                converted_error_message = str(message)
            message = converted_error_message

        return f"(API error) {message}"

    except Exception as exc:
        return f"Error retrieving APIError: {str(exc)}"
