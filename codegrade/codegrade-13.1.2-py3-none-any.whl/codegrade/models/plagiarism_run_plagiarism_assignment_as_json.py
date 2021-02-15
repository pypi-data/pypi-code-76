"""The module that defines the ``PlagiarismRunPlagiarismAssignmentAsJSON`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class PlagiarismRunPlagiarismAssignmentAsJSON:
    """This object represents an assignment that is connected to a plagiarism
    run or case.
    """

    #: The id of the assignment.
    id: "int"
    #: The name of the assignment
    name: "str"
    #: The id of the course the assignment is in.
    course_id: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of the assignment.",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The name of the assignment",
            ),
            rqa.RequiredArgument(
                "course_id",
                rqa.SimpleValue.int,
                doc="The id of the course the assignment is in.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["course_id"] = to_dict(self.course_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["PlagiarismRunPlagiarismAssignmentAsJSON"], d: Dict[str, Any]
    ) -> "PlagiarismRunPlagiarismAssignmentAsJSON":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
            course_id=parsed.course_id,
        )
        res.raw_data = d
        return res
