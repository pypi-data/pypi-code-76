"""The endpoints for comment objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from typing import TYPE_CHECKING, Any, Generic, Mapping, TypeVar, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from ..utils import get_error, log_warnings, response_code_matches, to_dict

if TYPE_CHECKING:
    from typing import Sequence

    from ..client import AuthenticatedClient, _BaseClient
    from ..models.base_error import BaseError
    from ..models.comment_reply_edit import CommentReplyEdit
    from ..parsers import JsonResponseParser, ParserFor

_ClientT = TypeVar("_ClientT", bound="_BaseClient")


class CommentService(Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all_reply_edits(
        self: "CommentService[AuthenticatedClient]",
        *,
        comment_base_id: "int",
        reply_id: "int",
        extra_parameters: Mapping[str, Union[str, bool, int, float]] = None,
    ) -> "Sequence[CommentReplyEdit]":
        """Get the edits of a reply.

        :param comment_base_id: The base of the given reply.
        :param reply_id: The id of the reply for which you want to get the
            replies.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A list of edits, sorted from newest to oldest.
        """
        from typing import Sequence

        from ..models.base_error import BaseError
        from ..models.comment_reply_edit import CommentReplyEdit
        from ..parsers import JsonResponseParser, ParserFor

        url = (
            "/api/v1/comments/{commentBaseId}/replies/{replyId}/edits/".format(
                commentBaseId=comment_base_id, replyId=reply_id
            )
        )
        params = extra_parameters or {}

        with self.__client as client:
            response = client.http.get(url=url, params=params)
        log_warnings(response)

        if response_code_matches(response.status_code, 200):
            return JsonResponseParser(
                rqa.List(ParserFor.make(CommentReplyEdit))
            ).try_parse(response)
        raise get_error(response, [((400, 409, 401, 403, "5XX"), BaseError)])
