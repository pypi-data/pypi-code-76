"""The module that defines the ``ResultDataGetTaskResultGetAll`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .extended_job import ExtendedJob


@dataclass
class ResultDataGetTaskResultGetAll:
    """The history of jobs for an instance."""

    #: Jobs that have not yet started
    not_started: "Sequence[ExtendedJob]"
    #: Jobs that are currently running.
    active: "Sequence[ExtendedJob]"
    #: A part of the jobs that have finished.
    finished: "Sequence[ExtendedJob]"
    #: The total amount of jobs that have finished.
    total_finished: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "not_started",
                rqa.List(ParserFor.make(ExtendedJob)),
                doc="Jobs that have not yet started",
            ),
            rqa.RequiredArgument(
                "active",
                rqa.List(ParserFor.make(ExtendedJob)),
                doc="Jobs that are currently running.",
            ),
            rqa.RequiredArgument(
                "finished",
                rqa.List(ParserFor.make(ExtendedJob)),
                doc="A part of the jobs that have finished.",
            ),
            rqa.RequiredArgument(
                "total_finished",
                rqa.SimpleValue.int,
                doc="The total amount of jobs that have finished.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["not_started"] = to_dict(self.not_started)
        res["active"] = to_dict(self.active)
        res["finished"] = to_dict(self.finished)
        res["total_finished"] = to_dict(self.total_finished)
        return res

    @classmethod
    def from_dict(
        cls: Type["ResultDataGetTaskResultGetAll"], d: Dict[str, Any]
    ) -> "ResultDataGetTaskResultGetAll":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            not_started=parsed.not_started,
            active=parsed.active,
            finished=parsed.finished,
            total_finished=parsed.total_finished,
        )
        res.raw_data = d
        return res
