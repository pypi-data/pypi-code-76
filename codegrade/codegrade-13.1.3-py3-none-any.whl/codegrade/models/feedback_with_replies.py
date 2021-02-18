"""The module that defines the ``FeedbackWithReplies`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .comment_base import CommentBase
from .feedback_base import FeedbackBase
from .user import User


@dataclass
class FeedbackWithReplies(FeedbackBase):
    """The JSON representation for feedback with replies."""

    #: A list of users that have given inline feedback on this submission.
    user: "Sequence[CommentBase]"
    #: A list of all authors you have permission to see that placed comments.
    #: This list is unique, i.e. each author occurs at most once.
    authors: "Sequence[User]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: FeedbackBase.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "user",
                    rqa.List(ParserFor.make(CommentBase)),
                    doc=(
                        "A list of users that have given inline feedback on"
                        " this submission."
                    ),
                ),
                rqa.RequiredArgument(
                    "authors",
                    rqa.List(ParserFor.make(User)),
                    doc=(
                        "A list of all authors you have permission to see that"
                        " placed comments. This list is unique, i.e. each"
                        " author occurs at most once."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["user"] = to_dict(self.user)
        res["authors"] = to_dict(self.authors)
        res["general"] = to_dict(self.general)
        res["linter"] = to_dict(self.linter)
        return res

    @classmethod
    def from_dict(
        cls: Type["FeedbackWithReplies"], d: Dict[str, Any]
    ) -> "FeedbackWithReplies":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            user=parsed.user,
            authors=parsed.authors,
            general=parsed.general,
            linter=parsed.linter,
        )
        res.raw_data = d
        return res
