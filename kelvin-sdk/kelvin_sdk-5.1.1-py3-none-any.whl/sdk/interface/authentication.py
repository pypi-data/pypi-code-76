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

from typeguard import typechecked


@typechecked
def reset() -> bool:
    """
    Reset all authentication and configuration cache.

    :return: a boolean indicating whether the reset was successfully performed..

    """

    from kelvin.sdk.lib.common.auth.auth_manager import reset_configurations as _reset_configurations

    return _reset_configurations()


@typechecked
def login(
    url: Optional[str], username: Optional[str], password: Optional[str], totp: Optional[str], reset: bool
) -> bool:
    """
    Logs the user into the provided url.

    :param url: the url to log on.
    :param username: the username of the client site.
    :param password: the password corresponding to the username.
    :param totp: the current TOTP corresponding to the username.
    :param reset: if set to True, will clear the existing configuration prior to the new session.

    :return: a boolean indicating whether the user was successfully logged in.

    """
    from kelvin.sdk.lib.common.auth.auth_manager import login_on_url as _login_on_url

    return _login_on_url(url=url, username=username, password=password, totp=totp, reset=reset)


@typechecked
def logout(ignore_destructive_warning: bool) -> bool:
    """
    Logs off the client all currently stored sessions.

    :param ignore_destructive_warning: indicates whether it should ignore the destructive warning.

    :return: a boolean indicating whether the user was successfully logged out.

    """
    from kelvin.sdk.lib.common.auth.auth_manager import logout_from_all_sessions as _logout_from_all_sessions

    return _logout_from_all_sessions(ignore_destructive_warning=ignore_destructive_warning)


@typechecked
def authentication_token(full: bool, margin: float) -> bool:
    """
    Obtain an authentication authentication_token from the API.

    :param full: return the full authentication_token.
    :param margin: minimum time to expiry.

    :return: a boolean indicating whether the authentication_token was successfully obtained.
    """

    from kelvin.sdk.lib.common.auth.auth_manager import authentication_token as _authentication_token

    return _authentication_token(full=full, margin=margin)
