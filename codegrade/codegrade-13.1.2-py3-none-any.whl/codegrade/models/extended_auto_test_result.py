"""The module that defines the ``ExtendedAutoTestResult`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_quality_comment import AutoTestQualityComment
from .auto_test_result import AutoTestResult
from .auto_test_step_result import AutoTestStepResult
from .file_tree import FileTree


@dataclass
class ExtendedAutoTestResult(AutoTestResult):
    """The extended JSON representation of a result."""

    #: The stdout produced in the student setup script.
    setup_stdout: "Optional[str]"
    #: The stderr produced in the student setup script.
    setup_stderr: "Optional[str]"
    #: The results for each step in this AutoTest. The ordering of this list is
    #: arbitrary, and the results for entire suites and or sets might be
    #: missing.
    step_results: "Sequence[AutoTestStepResult]"
    #: If the result has not started this will contain the amount of students
    #: we expect we still need to run before this result is next. This might be
    #: incorrect and should only be used as a rough estimate.
    approx_waiting_before: "Optional[int]"
    #: If `true` this is the final result for the student, meaning that without
    #: teacher interaction (e.g. restarting the AutoTest) this result will not
    #: change and will be used as is to calculate the grade of the student.
    #: Reasons why this may not be the case include but are not limited to the
    #: test containing hidden steps that will only be run after the deadline.
    final_result: "bool"
    #: A mapping between suite id and the files written to the AutoTest output
    #: folder in that suite.
    suite_files: "Mapping[str, Sequence[FileTree]]"
    #: The quality comments produced by this AutoTest result.
    quality_comments: "Sequence[AutoTestQualityComment]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: AutoTestResult.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "setup_stdout",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc="The stdout produced in the student setup script.",
                ),
                rqa.RequiredArgument(
                    "setup_stderr",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc="The stderr produced in the student setup script.",
                ),
                rqa.RequiredArgument(
                    "step_results",
                    rqa.List(ParserFor.make(AutoTestStepResult)),
                    doc=(
                        "The results for each step in this AutoTest. The"
                        " ordering of this list is arbitrary, and the results"
                        " for entire suites and or sets might be missing."
                    ),
                ),
                rqa.RequiredArgument(
                    "approx_waiting_before",
                    rqa.Nullable(rqa.SimpleValue.int),
                    doc=(
                        "If the result has not started this will contain the"
                        " amount of students we expect we still need to run"
                        " before this result is next. This might be incorrect"
                        " and should only be used as a rough estimate."
                    ),
                ),
                rqa.RequiredArgument(
                    "final_result",
                    rqa.SimpleValue.bool,
                    doc=(
                        "If `true` this is the final result for the student,"
                        " meaning that without teacher interaction (e.g."
                        " restarting the AutoTest) this result will not change"
                        " and will be used as is to calculate the grade of the"
                        " student. Reasons why this may not be the case"
                        " include but are not limited to the test containing"
                        " hidden steps that will only be run after the"
                        " deadline."
                    ),
                ),
                rqa.RequiredArgument(
                    "suite_files",
                    rqa.LookupMapping(rqa.List(ParserFor.make(FileTree))),
                    doc=(
                        "A mapping between suite id and the files written to"
                        " the AutoTest output folder in that suite."
                    ),
                ),
                rqa.RequiredArgument(
                    "quality_comments",
                    rqa.List(ParserFor.make(AutoTestQualityComment)),
                    doc=(
                        "The quality comments produced by this AutoTest"
                        " result."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["setup_stdout"] = to_dict(self.setup_stdout)
        res["setup_stderr"] = to_dict(self.setup_stderr)
        res["step_results"] = to_dict(self.step_results)
        res["approx_waiting_before"] = to_dict(self.approx_waiting_before)
        res["final_result"] = to_dict(self.final_result)
        res["suite_files"] = to_dict(self.suite_files)
        res["quality_comments"] = to_dict(self.quality_comments)
        res["id"] = to_dict(self.id)
        res["created_at"] = to_dict(self.created_at)
        res["started_at"] = to_dict(self.started_at)
        res["work_id"] = to_dict(self.work_id)
        res["state"] = to_dict(self.state)
        res["points_achieved"] = to_dict(self.points_achieved)
        return res

    @classmethod
    def from_dict(
        cls: Type["ExtendedAutoTestResult"], d: Dict[str, Any]
    ) -> "ExtendedAutoTestResult":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            setup_stdout=parsed.setup_stdout,
            setup_stderr=parsed.setup_stderr,
            step_results=parsed.step_results,
            approx_waiting_before=parsed.approx_waiting_before,
            final_result=parsed.final_result,
            suite_files=parsed.suite_files,
            quality_comments=parsed.quality_comments,
            id=parsed.id,
            created_at=parsed.created_at,
            started_at=parsed.started_at,
            work_id=parsed.work_id,
            state=parsed.state,
            points_achieved=parsed.points_achieved,
        )
        res.raw_data = d
        return res
