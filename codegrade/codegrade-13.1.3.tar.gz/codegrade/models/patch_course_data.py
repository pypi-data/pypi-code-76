"""The module that defines the ``PatchCourseData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor
from ..utils import to_dict
from .course_state import CourseState


@dataclass
class PatchCourseData:
    """"""

    #: The new name of the course
    name: Maybe["str"] = Nothing
    #: The new state of the course, currently you cannot set the state of a
    #: course to 'deleted'
    state: Maybe["CourseState"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.OptionalArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The new name of the course",
            ),
            rqa.OptionalArgument(
                "state",
                rqa.EnumValue(CourseState),
                doc=(
                    "The new state of the course, currently you cannot set the"
                    " state of a course to 'deleted'"
                ),
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.name = maybe_from_nullable(self.name)
        self.state = maybe_from_nullable(self.state)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        if self.name.is_just:
            res["name"] = to_dict(self.name.value)
        if self.state.is_just:
            res["state"] = to_dict(self.state.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["PatchCourseData"], d: Dict[str, Any]
    ) -> "PatchCourseData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            state=parsed.state,
        )
        res.raw_data = d
        return res
