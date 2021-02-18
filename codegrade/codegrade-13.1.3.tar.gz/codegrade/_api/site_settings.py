"""The endpoints for site_settings objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Union

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.all_site_settings import AllSiteSettings
    from ..models.base_error import BaseError
    from ..models.frontend_site_settings import FrontendSiteSettings
    from ..models.patch_site_settings_data import PatchSiteSettingsData
    from ..parsers import JsonResponseParser, ParserFor, make_union

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class SiteSettingsService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all(
        self: "SiteSettingsService[AuthenticatedClient]",
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[AllSiteSettings, FrontendSiteSettings]":
        """Get the settings for this CodeGrade instance.

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The site settings for this instance.
        """
        from typing import Union

        from ..models.all_site_settings import AllSiteSettings
        from ..models.base_error import BaseError
        from ..models.frontend_site_settings import FrontendSiteSettings
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/site_settings/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    ParserFor.make(AllSiteSettings),
                    ParserFor.make(FrontendSiteSettings),
                )
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])

    def patch(
        self: "SiteSettingsService[AuthenticatedClient]",
        json_body: Union[dict, list, "PatchSiteSettingsData"],
        *,
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Union[AllSiteSettings, FrontendSiteSettings]":
        """Update the settings for this CodeGrade instance.

        :param json_body: The body of the request. See
            :model:`.PatchSiteSettingsData` for information about the possible
            fields. You can provide this data as a
            :model:`.PatchSiteSettingsData` or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated site settings.
        """
        from typing import Union

        from ..models.all_site_settings import AllSiteSettings
        from ..models.base_error import BaseError
        from ..models.frontend_site_settings import FrontendSiteSettings
        from ..models.patch_site_settings_data import PatchSiteSettingsData
        from ..parsers import JsonResponseParser, ParserFor, make_union

        url = "/api/v1/site_settings/"
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.patch(
                url=url, json=to_dict(json_body), params=params
            )
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                make_union(
                    ParserFor.make(AllSiteSettings),
                    ParserFor.make(FrontendSiteSettings),
                )
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
