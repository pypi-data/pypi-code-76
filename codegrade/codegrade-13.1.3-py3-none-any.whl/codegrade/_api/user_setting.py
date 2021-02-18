"""The endpoints for user_setting objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Mapping, Optional

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.notification_setting import NotificationSetting
    from ..models.patch_notification_setting_user_setting_data import (
        PatchNotificationSettingUserSettingData,
    )
    from ..models.patch_ui_preference_user_setting_data import (
        PatchUiPreferenceUserSettingData,
    )
    from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class UserSettingService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all_notification_settings(
        self,
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "NotificationSetting":
        """Update preferences for notifications.

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The preferences for the user as described by the `token`.
        """
        from ..models.base_error import BaseError
        from ..models.notification_setting import NotificationSetting
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/settings/notification_settings/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                ParserFor.make(NotificationSetting)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def patch_notification_setting(
        self,
        json_body: Union[
            dict, list, "PatchNotificationSettingUserSettingData"
        ],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Update preferences for notifications.

        :param json_body: The body of the request. See
            :model:`.PatchNotificationSettingUserSettingData` for information
            about the possible fields. You can provide this data as a
            :model:`.PatchNotificationSettingUserSettingData` or as a
            dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from ..models.base_error import BaseError
        from ..models.patch_notification_setting_user_setting_data import (
            PatchNotificationSettingUserSettingData,
        )
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/settings/notification_settings/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_all_ui_preferences(
        self,
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Mapping[str, Optional[bool]]":
        """Get ui preferences.

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The preferences for the user as described by the `token`.
        """
        from typing import Mapping, Optional

        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/settings/ui_preferences/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.LookupMapping(rqa.Nullable(rqa.SimpleValue.bool))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def patch_ui_preference(
        self,
        json_body: Union[dict, list, "PatchUiPreferenceUserSettingData"],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "None":
        """Update ui preferences.

        :param json_body: The body of the request. See
            :model:`.PatchUiPreferenceUserSettingData` for information about
            the possible fields. You can provide this data as a
            :model:`.PatchUiPreferenceUserSettingData` or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """
        from ..models.base_error import BaseError
        from ..models.patch_ui_preference_user_setting_data import (
            PatchUiPreferenceUserSettingData,
        )
        from ..parsers import ConstantlyParser, JsonResponseParser, ParserFor

        url = "/api/v1/settings/ui_preferences/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 204):
            return ConstantlyParser(None).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def get_ui_preference(
        self,
        *,
        name: "str",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Optional[bool]":
        """Get a single UI preferences.

        :param name: The preference name you want to get.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The preferences for the user as described by the `token`.
        """
        from typing import Optional

        from ..models.base_error import BaseError
        from ..parsers import JsonResponseParser, ParserFor

        url = "/api/v1/settings/ui_preferences/{name}".format(name=name)
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.Nullable(rqa.SimpleValue.bool)
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
