"""The module that defines the ``ExtendedWork`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .user import User
from .work import Work
from .work_rubric_result_as_json import WorkRubricResultAsJSON


@dataclass
class ExtendedWork(Work):
    """A submission in CodeGrade with extended data.

    All data that might be `None` in this class might be `None` because of
    missing data or missing permissions.
    """

    #: The general feedback comment for this submission.
    comment: "Optional[str]"
    #: The author of the general feedback comment.
    comment_author: "Optional[User]"
    #: The assignment id of this submission.
    assignment_id: "int"
    #: The rubric result of this submission.
    rubric_result: "Optional[WorkRubricResultAsJSON]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: Work.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "comment",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc="The general feedback comment for this submission.",
                ),
                rqa.RequiredArgument(
                    "comment_author",
                    rqa.Nullable(ParserFor.make(User)),
                    doc="The author of the general feedback comment.",
                ),
                rqa.RequiredArgument(
                    "assignment_id",
                    rqa.SimpleValue.int,
                    doc="The assignment id of this submission.",
                ),
                rqa.RequiredArgument(
                    "rubric_result",
                    rqa.Nullable(ParserFor.make(WorkRubricResultAsJSON)),
                    doc="The rubric result of this submission.",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["comment"] = to_dict(self.comment)
        res["comment_author"] = to_dict(self.comment_author)
        res["assignment_id"] = to_dict(self.assignment_id)
        res["rubric_result"] = to_dict(self.rubric_result)
        res["id"] = to_dict(self.id)
        res["user"] = to_dict(self.user)
        res["origin"] = to_dict(self.origin)
        res["created_at"] = to_dict(self.created_at)
        res["grade"] = to_dict(self.grade)
        res["assignee"] = to_dict(self.assignee)
        res["grade_overridden"] = to_dict(self.grade_overridden)
        res["extra_info"] = to_dict(self.extra_info)
        return res

    @classmethod
    def from_dict(
        cls: Type["ExtendedWork"], d: Dict[str, Any]
    ) -> "ExtendedWork":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            comment=parsed.comment,
            comment_author=parsed.comment_author,
            assignment_id=parsed.assignment_id,
            rubric_result=parsed.rubric_result,
            id=parsed.id,
            user=parsed.user,
            origin=parsed.origin,
            created_at=parsed.created_at,
            grade=parsed.grade,
            assignee=parsed.assignee,
            grade_overridden=parsed.grade_overridden,
            extra_info=parsed.extra_info,
        )
        res.raw_data = d
        return res
