"""The module that defines the ``AssignmentFeedback`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class AssignmentFeedback:
    """The feedback of a single submission when getting all feedback through
    the `/assignments/{assignmentId}/feedbacks/` route.
    """

    #: The general feedback of the submission.
    general: "str"
    #: The inline comments as a list of strings.
    user: "Sequence[str]"
    #: The linter comments as a list of strings.
    linter: "Sequence[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "general",
                rqa.SimpleValue.str,
                doc="The general feedback of the submission.",
            ),
            rqa.RequiredArgument(
                "user",
                rqa.List(rqa.SimpleValue.str),
                doc="The inline comments as a list of strings.",
            ),
            rqa.RequiredArgument(
                "linter",
                rqa.List(rqa.SimpleValue.str),
                doc="The linter comments as a list of strings.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["general"] = to_dict(self.general)
        res["user"] = to_dict(self.user)
        res["linter"] = to_dict(self.linter)
        return res

    @classmethod
    def from_dict(
        cls: Type["AssignmentFeedback"], d: Dict[str, Any]
    ) -> "AssignmentFeedback":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            general=parsed.general,
            user=parsed.user,
            linter=parsed.linter,
        )
        res.raw_data = d
        return res
