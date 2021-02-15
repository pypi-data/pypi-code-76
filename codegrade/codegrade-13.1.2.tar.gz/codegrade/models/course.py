"""The module that defines the ``Course`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type, Union

import cg_request_args as rqa

from ..parsers import ParserFor, make_union
from ..utils import to_dict
from .course_state import CourseState
from .finalized_lti1p1_provider import FinalizedLTI1p1Provider
from .finalized_lti1p3_provider import FinalizedLTI1p3Provider
from .non_finalized_lti1p1_provider import NonFinalizedLTI1p1Provider
from .non_finalized_lti1p3_provider import NonFinalizedLTI1p3Provider


@dataclass
class Course:
    """The way this class will be represented in JSON."""

    #: The id of this course
    id: "int"
    #: The name of this course
    name: "str"
    #: The date this course was created
    created_at: "datetime.datetime"
    #: Is this a virtual course.
    virtual: "bool"
    #: The lti provider that manages this course, if `null` this is not a LTI
    #: course.
    lti_provider: "Optional[Union[NonFinalizedLTI1p3Provider, NonFinalizedLTI1p1Provider, FinalizedLTI1p3Provider, FinalizedLTI1p1Provider]]"
    #: The state this course is in.
    state: "CourseState"
    #: The id of the tenant that owns this course.
    tenant_id: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this course",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The name of this course",
            ),
            rqa.RequiredArgument(
                "created_at",
                rqa.RichValue.DateTime,
                doc="The date this course was created",
            ),
            rqa.RequiredArgument(
                "virtual",
                rqa.SimpleValue.bool,
                doc="Is this a virtual course.",
            ),
            rqa.RequiredArgument(
                "lti_provider",
                rqa.Nullable(
                    make_union(
                        ParserFor.make(NonFinalizedLTI1p3Provider),
                        ParserFor.make(NonFinalizedLTI1p1Provider),
                        ParserFor.make(FinalizedLTI1p3Provider),
                        ParserFor.make(FinalizedLTI1p1Provider),
                    )
                ),
                doc=(
                    "The lti provider that manages this course, if `null` this"
                    " is not a LTI course."
                ),
            ),
            rqa.RequiredArgument(
                "state",
                rqa.EnumValue(CourseState),
                doc="The state this course is in.",
            ),
            rqa.RequiredArgument(
                "tenant_id",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="The id of the tenant that owns this course.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["created_at"] = to_dict(self.created_at)
        res["virtual"] = to_dict(self.virtual)
        res["lti_provider"] = to_dict(self.lti_provider)
        res["state"] = to_dict(self.state)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(cls: Type["Course"], d: Dict[str, Any]) -> "Course":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
            created_at=parsed.created_at,
            virtual=parsed.virtual,
            lti_provider=parsed.lti_provider,
            state=parsed.state,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
