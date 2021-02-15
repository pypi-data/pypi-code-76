"""The endpoints for about objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Mapping, Union

import cg_request_args as rqa

from ..models.about import About
from ..models.base_error import BaseError
from ..parsers import JsonResponseParser, ParserFor
from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from ..client import Client


def get(
    *,
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "Client",
) -> About:
    """Get information about this CodeGrade instance.

    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The about object for this instance.
    """
    url = "/api/v1/about"
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(About)).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
