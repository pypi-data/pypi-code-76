"""The module that defines the ``ExtendedAutoTestRun`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_result import AutoTestResult
from .auto_test_run import AutoTestRun


@dataclass
class ExtendedAutoTestRun(AutoTestRun):
    """The run as extended JSON."""

    #: The results in this run. This will only contain the result for the
    #: latest submissions.
    results: "Sequence[AutoTestResult]"
    #: The stdout output of the `run_setup_script`
    setup_stdout: "str"
    #: The stderr output of the `run_setup_script`
    setup_stderr: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: AutoTestRun.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "results",
                    rqa.List(ParserFor.make(AutoTestResult)),
                    doc=(
                        "The results in this run. This will only contain the"
                        " result for the latest submissions."
                    ),
                ),
                rqa.RequiredArgument(
                    "setup_stdout",
                    rqa.SimpleValue.str,
                    doc="The stdout output of the `run_setup_script`",
                ),
                rqa.RequiredArgument(
                    "setup_stderr",
                    rqa.SimpleValue.str,
                    doc="The stderr output of the `run_setup_script`",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["results"] = to_dict(self.results)
        res["setup_stdout"] = to_dict(self.setup_stdout)
        res["setup_stderr"] = to_dict(self.setup_stderr)
        res["id"] = to_dict(self.id)
        res["created_at"] = to_dict(self.created_at)
        res["state"] = to_dict(self.state)
        res["is_continuous"] = to_dict(self.is_continuous)
        return res

    @classmethod
    def from_dict(
        cls: Type["ExtendedAutoTestRun"], d: Dict[str, Any]
    ) -> "ExtendedAutoTestRun":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            results=parsed.results,
            setup_stdout=parsed.setup_stdout,
            setup_stderr=parsed.setup_stderr,
            id=parsed.id,
            created_at=parsed.created_at,
            state=parsed.state,
            is_continuous=parsed.is_continuous,
        )
        res.raw_data = d
        return res
