"""The module that defines the ``PlagiarismRunPlagiarismCourseAsJSON`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class PlagiarismRunPlagiarismCourseAsJSON:
    """This object represents an course that is connected to a plagiarism run
    or case.
    """

    #: The id of the course
    id: "int"
    #: The name of the course.
    name: "str"
    #: Is this is a virtual course?
    virtual: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of the course",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The name of the course.",
            ),
            rqa.RequiredArgument(
                "virtual",
                rqa.SimpleValue.bool,
                doc="Is this is a virtual course?",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["virtual"] = to_dict(self.virtual)
        return res

    @classmethod
    def from_dict(
        cls: Type["PlagiarismRunPlagiarismCourseAsJSON"], d: Dict[str, Any]
    ) -> "PlagiarismRunPlagiarismCourseAsJSON":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
            virtual=parsed.virtual,
        )
        res.raw_data = d
        return res
