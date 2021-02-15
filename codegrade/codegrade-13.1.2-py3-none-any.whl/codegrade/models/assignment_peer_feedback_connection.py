"""The module that defines the ``AssignmentPeerFeedbackConnection`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .user import User


@dataclass
class AssignmentPeerFeedbackConnection:
    """A peer feedback connection that connects two students."""

    #: The user that should be given a review.
    subject: "User"
    #: The user that should do the review.
    peer: "User"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "subject",
                ParserFor.make(User),
                doc="The user that should be given a review.",
            ),
            rqa.RequiredArgument(
                "peer",
                ParserFor.make(User),
                doc="The user that should do the review.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["subject"] = to_dict(self.subject)
        res["peer"] = to_dict(self.peer)
        return res

    @classmethod
    def from_dict(
        cls: Type["AssignmentPeerFeedbackConnection"], d: Dict[str, Any]
    ) -> "AssignmentPeerFeedbackConnection":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            subject=parsed.subject,
            peer=parsed.peer,
        )
        res.raw_data = d
        return res
