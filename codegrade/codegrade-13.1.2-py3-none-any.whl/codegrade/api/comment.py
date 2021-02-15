"""The endpoints for comment objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Mapping, Sequence, Union

import cg_request_args as rqa

from ..models.base_error import BaseError
from ..models.comment_reply_edit import CommentReplyEdit
from ..parsers import JsonResponseParser, ParserFor
from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from ..client import AuthenticatedClient


def get_all_reply_edits(
    *,
    comment_base_id: "int",
    reply_id: "int",
    extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    client: "AuthenticatedClient",
) -> Sequence[CommentReplyEdit]:
    """Get the edits of a reply.

    :param comment_base_id: The base of the given reply.
    :param reply_id: The id of the reply for which you want to get the replies.
    :param extra_parameters: The extra query parameters you might want to add.
        By default no extra query parameters are added.
    :param client: The client to do the request with. If you access this method
        through the client you should not pass this argument.

    :returns: A list of edits, sorted from newest to oldest.
    """
    url = "/api/v1/comments/{commentBaseId}/replies/{replyId}/edits/".format(
        commentBaseId=comment_base_id, replyId=reply_id
    )
    params = extra_parameters or {}

    response = client.http.get(url=url, params=params)
    log_warnings(response)

    if response_code_matches(response.status_code, 200):
        return JsonResponseParser(
            rqa.List(ParserFor.make(CommentReplyEdit))
        ).try_parse(response)
    raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
