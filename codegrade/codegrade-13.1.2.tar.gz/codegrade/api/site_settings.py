"""The endpoints for site_settings objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Mapping, Union

import cg_request_args as rqa

from ..models.all_site_settings import AllSiteSettings
from ..models.base_error import BaseError
from ..models.frontend_site_settings import FrontendSiteSettings
from ..models.patch_site_settings_data import PatchSiteSettingsData
from ..parsers import JsonResponseParser, ParserFor, make_union
from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from ..client import AuthenticatedClient


def get_all(
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Union[AllSiteSettings, FrontendSiteSettings]:
    """Get the settings for this CodeGrade instance.

    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The site settings for this instance.
    """
    url = "/api/v1/site_settings/"
    params = extra_parameters or {}

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
    json_body: PatchSiteSettingsData,
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Union[AllSiteSettings, FrontendSiteSettings]:
    """Update the settings for this CodeGrade instance.

    :param json_body: The body of the request. See
        :model:`.PatchSiteSettingsData` for information about the possible
        fields. You can provide this data as a :model:`.PatchSiteSettingsData`
        or as a dictionary.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The updated site settings.
    """
    url = "/api/v1/site_settings/"
    params = extra_parameters or {}

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
