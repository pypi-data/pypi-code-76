"""The module that defines the ``UserCourse`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .course_role import CourseRole
from .user import User


@dataclass
class UserCourse:
    """The result returned when adding a user to a course."""

    #: The User that was added.
    user: "User"
    #: The role that the user got.
    course_role: "CourseRole"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "User",
                ParserFor.make(User),
                doc="The User that was added.",
            ),
            rqa.RequiredArgument(
                "CourseRole",
                ParserFor.make(CourseRole),
                doc="The role that the user got.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["User"] = to_dict(self.user)
        res["CourseRole"] = to_dict(self.course_role)
        return res

    @classmethod
    def from_dict(cls: Type["UserCourse"], d: Dict[str, Any]) -> "UserCourse":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            user=parsed.User,
            course_role=parsed.CourseRole,
        )
        res.raw_data = d
        return res
