"""The module that defines the ``CourseRegistrationLink`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .course_role import CourseRole


@dataclass
class CourseRegistrationLink:
    """The JSON representation of a course registration link."""

    #: The id of this link
    id: "str"
    #: The moment this link will stop working
    expiration_date: "datetime.datetime"
    #: The role new users will get
    role: "CourseRole"
    #: Can users register with this link
    allow_register: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc="The id of this link",
            ),
            rqa.RequiredArgument(
                "expiration_date",
                rqa.RichValue.DateTime,
                doc="The moment this link will stop working",
            ),
            rqa.RequiredArgument(
                "role",
                ParserFor.make(CourseRole),
                doc="The role new users will get",
            ),
            rqa.RequiredArgument(
                "allow_register",
                rqa.SimpleValue.bool,
                doc="Can users register with this link",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["expiration_date"] = to_dict(self.expiration_date)
        res["role"] = to_dict(self.role)
        res["allow_register"] = to_dict(self.allow_register)
        return res

    @classmethod
    def from_dict(
        cls: Type["CourseRegistrationLink"], d: Dict[str, Any]
    ) -> "CourseRegistrationLink":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            expiration_date=parsed.expiration_date,
            role=parsed.role,
            allow_register=parsed.allow_register,
        )
        res.raw_data = d
        return res
