"""The module that defines the ``AutoTestSet`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .auto_test_suite import AutoTestSuite


@dataclass
class AutoTestSet:
    """The result as JSON."""

    #: The id of this set.
    id: "int"
    #: The suites connected to this set. In the UI these are called
    #: "categories"
    suites: "Sequence[AutoTestSuite]"
    #: A floating indicating the minimum percentage of points a student should
    #: achieve after this set (or "level"). If this percentage is not achieved
    #: the AutoTest will stop running.
    stop_points: "float"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this set.",
            ),
            rqa.RequiredArgument(
                "suites",
                rqa.List(ParserFor.make(AutoTestSuite)),
                doc=(
                    "The suites connected to this set. In the UI these are"
                    ' called "categories"'
                ),
            ),
            rqa.RequiredArgument(
                "stop_points",
                rqa.SimpleValue.float,
                doc=(
                    "A floating indicating the minimum percentage of points a"
                    ' student should achieve after this set (or "level"). If'
                    " this percentage is not achieved the AutoTest will stop"
                    " running."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["suites"] = to_dict(self.suites)
        res["stop_points"] = to_dict(self.stop_points)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestSet"], d: Dict[str, Any]
    ) -> "AutoTestSet":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            suites=parsed.suites,
            stop_points=parsed.stop_points,
        )
        res.raw_data = d
        return res
