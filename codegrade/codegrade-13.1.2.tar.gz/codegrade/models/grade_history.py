"""The module that defines the ``GradeHistory`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .grade_origin import GradeOrigin
from .user import User


@dataclass
class GradeHistory:
    """A history event for the grade of a submission."""

    #: The moment the grade was changed.
    changed_at: "datetime.datetime"
    #: Was this grade given by a rubric.
    is_rubric: "Optional[bool]"
    #: What grade was given.
    grade: "Optional[float]"
    #: Has this grade been passed back to the LMS?
    passed_back: "Optional[bool]"
    #: What as the origin of the grade.
    origin: "GradeOrigin"
    #: The user that gave the grade, only available when `grade_origin` is
    #: `human`.
    user: "Optional[User]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "changed_at",
                rqa.RichValue.DateTime,
                doc="The moment the grade was changed.",
            ),
            rqa.RequiredArgument(
                "is_rubric",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="Was this grade given by a rubric.",
            ),
            rqa.RequiredArgument(
                "grade",
                rqa.Nullable(rqa.SimpleValue.float),
                doc="What grade was given.",
            ),
            rqa.RequiredArgument(
                "passed_back",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="Has this grade been passed back to the LMS?",
            ),
            rqa.RequiredArgument(
                "origin",
                rqa.EnumValue(GradeOrigin),
                doc="What as the origin of the grade.",
            ),
            rqa.RequiredArgument(
                "user",
                rqa.Nullable(ParserFor.make(User)),
                doc=(
                    "The user that gave the grade, only available when"
                    " `grade_origin` is `human`."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["changed_at"] = to_dict(self.changed_at)
        res["is_rubric"] = to_dict(self.is_rubric)
        res["grade"] = to_dict(self.grade)
        res["passed_back"] = to_dict(self.passed_back)
        res["origin"] = to_dict(self.origin)
        res["user"] = to_dict(self.user)
        return res

    @classmethod
    def from_dict(
        cls: Type["GradeHistory"], d: Dict[str, Any]
    ) -> "GradeHistory":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            changed_at=parsed.changed_at,
            is_rubric=parsed.is_rubric,
            grade=parsed.grade,
            passed_back=parsed.passed_back,
            origin=parsed.origin,
            user=parsed.user,
        )
        res.raw_data = d
        return res
