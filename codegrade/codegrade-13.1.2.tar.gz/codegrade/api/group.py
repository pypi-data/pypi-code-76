"""The endpoints for group objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Mapping, Union

import cg_request_args as rqa

from ..models.base_error import BaseError
from ..models.extended_group import ExtendedGroup
from ..models.user_input import UserInput
from ..parsers import JsonResponseParser, ParserFor
from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from ..client import AuthenticatedClient


def add_member(
    json_body: UserInput,
    *,
    group_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> ExtendedGroup:
    """Add a user (member) to a group.

    :param json_body: The body of the request. See :model:`.UserInput` for
        information about the possible fields. You can provide this data as a
        :model:`.UserInput` or as a dictionary.
    :param group_id: The id of the group the user should be added to.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The group with the newly added user.
    """
    url = "/api/v1/groups/{groupId}/member".format(groupId=group_id)
    params = extra_parameters or {}

    response = client.http.post(
        url=url, json=to_dict(json_body), params=params
    )
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(ExtendedGroup)).try_parse(
            response
        )
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])


def get(
    *,
    group_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> ExtendedGroup:
    """Get a group by id.

    :param group_id: The id of the group to get.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: The requested group.
    """
    url = "/api/v1/groups/{groupId}".format(groupId=group_id)
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(ParserFor.make(ExtendedGroup)).try_parse(
            response
        )
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
