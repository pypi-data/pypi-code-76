"""The module that defines the ``CourseRole`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .abstract_role import AbstractRole
from .course import Course


@dataclass
class CourseRole(AbstractRole):
    """The JSON representation of a course role."""

    #: The course this role is connected to
    course: "Course"
    #: Is this role hidden
    hidden: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: AbstractRole.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "course",
                    ParserFor.make(Course),
                    doc="The course this role is connected to",
                ),
                rqa.RequiredArgument(
                    "hidden",
                    rqa.SimpleValue.bool,
                    doc="Is this role hidden",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["course"] = to_dict(self.course)
        res["hidden"] = to_dict(self.hidden)
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        return res

    @classmethod
    def from_dict(cls: Type["CourseRole"], d: Dict[str, Any]) -> "CourseRole":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            course=parsed.course,
            hidden=parsed.hidden,
            id=parsed.id,
            name=parsed.name,
        )
        res.raw_data = d
        return res
