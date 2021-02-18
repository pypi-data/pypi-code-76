"""The module that defines the ``AssignmentPeerFeedbackSettings`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class AssignmentPeerFeedbackSettings:
    """The peer feedback settings for an assignment."""

    #: The amount of student that a single user should peer review.
    amount: "int"
    #: The amount of time in seconds a user has after the deadline to do the
    #: peer review.
    time: "Optional[float]"
    #: Should new peer feedback comments be considered approved by default or
    #: not.
    auto_approved: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "amount",
                rqa.SimpleValue.int,
                doc=(
                    "The amount of student that a single user should peer"
                    " review."
                ),
            ),
            rqa.RequiredArgument(
                "time",
                rqa.Nullable(rqa.SimpleValue.float),
                doc=(
                    "The amount of time in seconds a user has after the"
                    " deadline to do the peer review."
                ),
            ),
            rqa.RequiredArgument(
                "auto_approved",
                rqa.SimpleValue.bool,
                doc=(
                    "Should new peer feedback comments be considered approved"
                    " by default or not."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["amount"] = to_dict(self.amount)
        res["time"] = to_dict(self.time)
        res["auto_approved"] = to_dict(self.auto_approved)
        return res

    @classmethod
    def from_dict(
        cls: Type["AssignmentPeerFeedbackSettings"], d: Dict[str, Any]
    ) -> "AssignmentPeerFeedbackSettings":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            amount=parsed.amount,
            time=parsed.time,
            auto_approved=parsed.auto_approved,
        )
        res.raw_data = d
        return res
