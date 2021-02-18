"""The module that defines the ``ResultDataGetAutoTestGet`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_fixture import AutoTestFixture
from .auto_test_set import AutoTestSet
from .extended_auto_test_run import ExtendedAutoTestRun


@dataclass
class ResultDataGetAutoTestGet:
    """An AutoTest as JSON."""

    #: This id of this AutoTest
    id: "int"
    #: The fixtures connected to this AutoTest
    fixtures: "Sequence[AutoTestFixture]"
    #: The setup script that will be executed before any test starts.
    run_setup_script: "str"
    #: The setup script that will be executed for each student. In this script
    #: the submission of the student is available.
    setup_script: "str"
    #: Unused
    finalize_script: "str"
    #: The way the grade is calculated in this AutoTest. This is `null` if the
    #: options is still unset. This can be 'full' or 'partial'.
    grade_calculation: "Optional[str]"
    #: The sets in this AutoTest. In the UI these are called levels.
    sets: "Sequence[AutoTestSet]"
    #: The id of the assignment to which this AutoTest belongs.
    assignment_id: "int"
    #: The runs done with this AutoTest. This is list is always of length 0 or
    #: 1
    runs: "Sequence[ExtendedAutoTestRun]"
    #: If `true` This is `null` if the options is still unset.
    results_always_visible: "Optional[bool]"
    #: If `true` This is `null` if the options is still unset.
    prefer_teacher_revision: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="This id of this AutoTest",
            ),
            rqa.RequiredArgument(
                "fixtures",
                rqa.List(ParserFor.make(AutoTestFixture)),
                doc="The fixtures connected to this AutoTest",
            ),
            rqa.RequiredArgument(
                "run_setup_script",
                rqa.SimpleValue.str,
                doc=(
                    "The setup script that will be executed before any test"
                    " starts."
                ),
            ),
            rqa.RequiredArgument(
                "setup_script",
                rqa.SimpleValue.str,
                doc=(
                    "The setup script that will be executed for each student."
                    " In this script the submission of the student is"
                    " available."
                ),
            ),
            rqa.RequiredArgument(
                "finalize_script",
                rqa.SimpleValue.str,
                doc="Unused",
            ),
            rqa.RequiredArgument(
                "grade_calculation",
                rqa.Nullable(rqa.SimpleValue.str),
                doc=(
                    "The way the grade is calculated in this AutoTest. This is"
                    " `null` if the options is still unset. This can be 'full'"
                    " or 'partial'."
                ),
            ),
            rqa.RequiredArgument(
                "sets",
                rqa.List(ParserFor.make(AutoTestSet)),
                doc=(
                    "The sets in this AutoTest. In the UI these are called"
                    " levels."
                ),
            ),
            rqa.RequiredArgument(
                "assignment_id",
                rqa.SimpleValue.int,
                doc="The id of the assignment to which this AutoTest belongs.",
            ),
            rqa.RequiredArgument(
                "runs",
                rqa.List(ParserFor.make(ExtendedAutoTestRun)),
                doc=(
                    "The runs done with this AutoTest. This is list is always"
                    " of length 0 or 1"
                ),
            ),
            rqa.RequiredArgument(
                "results_always_visible",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="If `true` This is `null` if the options is still unset.",
            ),
            rqa.RequiredArgument(
                "prefer_teacher_revision",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="If `true` This is `null` if the options is still unset.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["fixtures"] = to_dict(self.fixtures)
        res["run_setup_script"] = to_dict(self.run_setup_script)
        res["setup_script"] = to_dict(self.setup_script)
        res["finalize_script"] = to_dict(self.finalize_script)
        res["grade_calculation"] = to_dict(self.grade_calculation)
        res["sets"] = to_dict(self.sets)
        res["assignment_id"] = to_dict(self.assignment_id)
        res["runs"] = to_dict(self.runs)
        res["results_always_visible"] = to_dict(self.results_always_visible)
        res["prefer_teacher_revision"] = to_dict(self.prefer_teacher_revision)
        return res

    @classmethod
    def from_dict(
        cls: Type["ResultDataGetAutoTestGet"], d: Dict[str, Any]
    ) -> "ResultDataGetAutoTestGet":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            fixtures=parsed.fixtures,
            run_setup_script=parsed.run_setup_script,
            setup_script=parsed.setup_script,
            finalize_script=parsed.finalize_script,
            grade_calculation=parsed.grade_calculation,
            sets=parsed.sets,
            assignment_id=parsed.assignment_id,
            runs=parsed.runs,
            results_always_visible=parsed.results_always_visible,
            prefer_teacher_revision=parsed.prefer_teacher_revision,
        )
        res.raw_data = d
        return res
