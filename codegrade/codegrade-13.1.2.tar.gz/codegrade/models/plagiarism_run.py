"""The module that defines the ``PlagiarismRun`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Mapping, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .assignment import Assignment
from .plagiarism_run_plagiarism_assignment_as_json import (
    PlagiarismRunPlagiarismAssignmentAsJSON,
)
from .plagiarism_run_plagiarism_course_as_json import (
    PlagiarismRunPlagiarismCourseAsJSON,
)
from .plagiarism_state import PlagiarismState


@dataclass
class PlagiarismRun:
    """The way this class will be represented in JSON."""

    #: The id of the run.
    id: "int"
    #: The state this run is in.
    state: "PlagiarismState"
    #: The amount of submissions that have finished the current state.
    submissions_done: "Optional[int]"
    #: The total amount of submissions connected to this run.
    submissions_total: "Optional[int]"
    #: Which provider is doing this run.
    provider_name: "str"
    #: The config used for this run.
    config: "Any"
    #: The time this run was created.
    created_at: "datetime.datetime"
    #: The assignment this run was done on.
    assignment: "Assignment"
    #: The log produced by the provider while running.
    log: "Optional[str]"
    #: A mapping between assignment id and the assignment for each assignment
    #: that is connected to this run. These are not (\!) full assignment
    #: objects, but only contain the `name` and `id`.
    assignments: "Mapping[str, PlagiarismRunPlagiarismAssignmentAsJSON]"
    #: The mapping between course id and the course for each course that is
    #: connected to this run. These are not (\!) full course object, but
    #: contain only the `name`, `id` and if the course is virtual.
    courses: "Mapping[str, PlagiarismRunPlagiarismCourseAsJSON]"
    #: If we found more matches than the maximum allowed (i.e. matches were
    #: dropped) this value is set to `True`.
    cases_dropped: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of the run.",
            ),
            rqa.RequiredArgument(
                "state",
                rqa.EnumValue(PlagiarismState),
                doc="The state this run is in.",
            ),
            rqa.RequiredArgument(
                "submissions_done",
                rqa.Nullable(rqa.SimpleValue.int),
                doc=(
                    "The amount of submissions that have finished the current"
                    " state."
                ),
            ),
            rqa.RequiredArgument(
                "submissions_total",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="The total amount of submissions connected to this run.",
            ),
            rqa.RequiredArgument(
                "provider_name",
                rqa.SimpleValue.str,
                doc="Which provider is doing this run.",
            ),
            rqa.RequiredArgument(
                "config",
                rqa.AnyValue,
                doc="The config used for this run.",
            ),
            rqa.RequiredArgument(
                "created_at",
                rqa.RichValue.DateTime,
                doc="The time this run was created.",
            ),
            rqa.RequiredArgument(
                "assignment",
                ParserFor.make(Assignment),
                doc="The assignment this run was done on.",
            ),
            rqa.RequiredArgument(
                "log",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="The log produced by the provider while running.",
            ),
            rqa.RequiredArgument(
                "assignments",
                rqa.LookupMapping(
                    ParserFor.make(PlagiarismRunPlagiarismAssignmentAsJSON)
                ),
                doc=(
                    "A mapping between assignment id and the assignment for"
                    " each assignment that is connected to this run. These are"
                    " not (\\!) full assignment objects, but only contain the"
                    " `name` and `id`."
                ),
            ),
            rqa.RequiredArgument(
                "courses",
                rqa.LookupMapping(
                    ParserFor.make(PlagiarismRunPlagiarismCourseAsJSON)
                ),
                doc=(
                    "The mapping between course id and the course for each"
                    " course that is connected to this run. These are not"
                    " (\\!) full course object, but contain only the `name`,"
                    " `id` and if the course is virtual."
                ),
            ),
            rqa.RequiredArgument(
                "cases_dropped",
                rqa.SimpleValue.bool,
                doc=(
                    "If we found more matches than the maximum allowed (i.e."
                    " matches were dropped) this value is set to `True`."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["state"] = to_dict(self.state)
        res["submissions_done"] = to_dict(self.submissions_done)
        res["submissions_total"] = to_dict(self.submissions_total)
        res["provider_name"] = to_dict(self.provider_name)
        res["config"] = to_dict(self.config)
        res["created_at"] = to_dict(self.created_at)
        res["assignment"] = to_dict(self.assignment)
        res["log"] = to_dict(self.log)
        res["assignments"] = to_dict(self.assignments)
        res["courses"] = to_dict(self.courses)
        res["cases_dropped"] = to_dict(self.cases_dropped)
        return res

    @classmethod
    def from_dict(
        cls: Type["PlagiarismRun"], d: Dict[str, Any]
    ) -> "PlagiarismRun":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            state=parsed.state,
            submissions_done=parsed.submissions_done,
            submissions_total=parsed.submissions_total,
            provider_name=parsed.provider_name,
            config=parsed.config,
            created_at=parsed.created_at,
            assignment=parsed.assignment,
            log=parsed.log,
            assignments=parsed.assignments,
            courses=parsed.courses,
            cases_dropped=parsed.cases_dropped,
        )
        res.raw_data = d
        return res
