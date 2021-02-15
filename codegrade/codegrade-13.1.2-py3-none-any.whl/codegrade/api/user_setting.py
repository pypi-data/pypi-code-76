"""The endpoints for user_setting objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Mapping, Optional, Union

import cg_request_args as rqa

from ..models.base_error import BaseError
from ..models.notification_setting import NotificationSetting
from ..models.patch_notification_setting_user_setting_data import (
    PatchNotificationSettingUserSettingData,
)
from ..models.patch_ui_preference_user_setting_data import (
    PatchUiPreferenceUserSettingData,
)
from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor
from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from ..client import Client


def get_all_notification_settings(
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "Client",
) -> NotificationSetting:
    """Update preferences for notifications.

    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The preferences for the user as described by the `token`.
    """
    url = "/api/v1/settings/notification_settings/"
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            ParserFor.make(NotificationSetting)
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def patch_notification_setting(
    json_body: PatchNotificationSettingUserSettingData,
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "Client",
) -> None:
    """Update preferences for notifications.

    :param json_body: The body of the request. See
        :model:`.PatchNotificationSettingUserSettingData` for information about
        the possible fields. You can provide this data as a
        :model:`.PatchNotificationSettingUserSettingData` or as a dictionary.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: Nothing.
    """
    url = "/api/v1/settings/notification_settings/"
    params = extra_parameters or {}

    response = client.http.patch(
        url=url, json=to_dict(json_body), params=params
    )
    log_warnings(response)

    if response_code_matches(response.status_code, 204):
        return ConstantlyParser(None).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_all_ui_preferences(
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "Client",
) -> Mapping[str, Optional[bool]]:
    """Get ui preferences.

    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The preferences for the user as described by the `token`.
    """
    url = "/api/v1/settings/ui_preferences/"
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            rqa.LookupMapping(rqa.Nullable(rqa.SimpleValue.bool))
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def patch_ui_preference(
    json_body: PatchUiPreferenceUserSettingData,
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "Client",
) -> None:
    """Update ui preferences.

    :param json_body: The body of the request. See
        :model:`.PatchUiPreferenceUserSettingData` for information about the
        possible fields. You can provide this data as a
        :model:`.PatchUiPreferenceUserSettingData` or as a dictionary.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: Nothing.
    """
    url = "/api/v1/settings/ui_preferences/"
    params = extra_parameters or {}

    response = client.http.patch(
        url=url, json=to_dict(json_body), params=params
    )
    log_warnings(response)

    if response_code_matches(response.status_code, 204):
        return ConstantlyParser(None).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get_ui_preference(
    *,
    name: "str",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "Client",
) -> Optional[bool]:
    """Get a single UI preferences.

    :param name: The preference name you want to get.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The preferences for the user as described by the `token`.
    """
    url = "/api/v1/settings/ui_preferences/{name}".format(name=name)
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            rqa.Nullable(rqa.SimpleValue.bool)
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
