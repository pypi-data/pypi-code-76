"""The module that defines the ``CommentBase`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .comment_reply import CommentReply


@dataclass
class CommentBase:
    """A comment thread, this contains many replies which contain the actual
    feedback.
    """

    #: The id of the comment base.
    id: "int"
    #: The line on which the comment was placed.
    line: "int"
    #: The id of the file on which this comment was placed.
    file_id: "str"
    #: The id of the work that this comment was placed on. This work will
    #: always contain the file with `file_id`.
    work_id: "int"
    #: The replies, that you are allowed to see, in this comment base.
    replies: "Sequence[CommentReply]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of the comment base.",
            ),
            rqa.RequiredArgument(
                "line",
                rqa.SimpleValue.int,
                doc="The line on which the comment was placed.",
            ),
            rqa.RequiredArgument(
                "file_id",
                rqa.SimpleValue.str,
                doc="The id of the file on which this comment was placed.",
            ),
            rqa.RequiredArgument(
                "work_id",
                rqa.SimpleValue.int,
                doc=(
                    "The id of the work that this comment was placed on. This"
                    " work will always contain the file with `file_id`."
                ),
            ),
            rqa.RequiredArgument(
                "replies",
                rqa.List(ParserFor.make(CommentReply)),
                doc=(
                    "The replies, that you are allowed to see, in this comment"
                    " base."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["line"] = to_dict(self.line)
        res["file_id"] = to_dict(self.file_id)
        res["work_id"] = to_dict(self.work_id)
        res["replies"] = to_dict(self.replies)
        return res

    @classmethod
    def from_dict(
        cls: Type["CommentBase"], d: Dict[str, Any]
    ) -> "CommentBase":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            line=parsed.line,
            file_id=parsed.file_id,
            work_id=parsed.work_id,
            replies=parsed.replies,
        )
        res.raw_data = d
        return res
