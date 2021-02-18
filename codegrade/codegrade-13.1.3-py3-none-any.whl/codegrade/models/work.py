"""The module that defines the ``Work`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .user import User
from .work_origin import WorkOrigin


@dataclass
class Work:
    """A submission in CodeGrade."""

    #: The id of the submission
    id: "int"
    #: The author of the submission. If submission was created by a group this
    #: will be the virtual user of the group.
    user: "User"
    #: The way this submission was created.
    origin: "WorkOrigin"
    #: The moment the submission was created.
    created_at: "datetime.datetime"
    #: The grade of the submission, or `None` if the submission hasn't been
    #: graded of you cannot see the grade.
    grade: "Optional[float]"
    #: The user assigned to this submission. Or `None` if not assigned or if
    #: you may not see the assignee.
    assignee: "Optional[User]"
    #: Does this submission have a rubric grade which has been overridden.
    grade_overridden: "bool"
    #: Some extra info that might be available. Currently only used for git
    #: submissions.
    extra_info: "Any"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of the submission",
            ),
            rqa.RequiredArgument(
                "user",
                ParserFor.make(User),
                doc=(
                    "The author of the submission. If submission was created"
                    " by a group this will be the virtual user of the group."
                ),
            ),
            rqa.RequiredArgument(
                "origin",
                rqa.EnumValue(WorkOrigin),
                doc="The way this submission was created.",
            ),
            rqa.RequiredArgument(
                "created_at",
                rqa.RichValue.DateTime,
                doc="The moment the submission was created.",
            ),
            rqa.RequiredArgument(
                "grade",
                rqa.Nullable(rqa.SimpleValue.float),
                doc=(
                    "The grade of the submission, or `None` if the submission"
                    " hasn't been graded of you cannot see the grade."
                ),
            ),
            rqa.RequiredArgument(
                "assignee",
                rqa.Nullable(ParserFor.make(User)),
                doc=(
                    "The user assigned to this submission. Or `None` if not"
                    " assigned or if you may not see the assignee."
                ),
            ),
            rqa.RequiredArgument(
                "grade_overridden",
                rqa.SimpleValue.bool,
                doc=(
                    "Does this submission have a rubric grade which has been"
                    " overridden."
                ),
            ),
            rqa.RequiredArgument(
                "extra_info",
                rqa.AnyValue,
                doc=(
                    "Some extra info that might be available. Currently only"
                    " used for git submissions."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
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
    def from_dict(cls: Type["Work"], d: Dict[str, Any]) -> "Work":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
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
