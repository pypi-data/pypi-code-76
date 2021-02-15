"""The module that defines the ``ExtendedJob`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Mapping, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict
from .job import Job


@dataclass
class ExtendedJob(Job):
    """The extended JSON serialization of a job."""

    #: The name of the job.
    name: "str"
    #: The kwargs given to the job.
    kwargs: "Mapping[str, Any]"
    #: The current try of the job.
    try_n: "int"
    #: The time the job should be executed.
    eta: "datetime.datetime"
    #: Possibly the traceback of the job. Only not `null` when the job failed.
    traceback: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: Job.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "name",
                    rqa.SimpleValue.str,
                    doc="The name of the job.",
                ),
                rqa.RequiredArgument(
                    "kwargs",
                    rqa.LookupMapping(rqa.AnyValue),
                    doc="The kwargs given to the job.",
                ),
                rqa.RequiredArgument(
                    "try_n",
                    rqa.SimpleValue.int,
                    doc="The current try of the job.",
                ),
                rqa.RequiredArgument(
                    "eta",
                    rqa.RichValue.DateTime,
                    doc="The time the job should be executed.",
                ),
                rqa.RequiredArgument(
                    "traceback",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc=(
                        "Possibly the traceback of the job. Only not `null`"
                        " when the job failed."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["kwargs"] = to_dict(self.kwargs)
        res["try_n"] = to_dict(self.try_n)
        res["eta"] = to_dict(self.eta)
        res["traceback"] = to_dict(self.traceback)
        res["id"] = to_dict(self.id)
        res["state"] = to_dict(self.state)
        res["result"] = to_dict(self.result)
        return res

    @classmethod
    def from_dict(
        cls: Type["ExtendedJob"], d: Dict[str, Any]
    ) -> "ExtendedJob":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            kwargs=parsed.kwargs,
            try_n=parsed.try_n,
            eta=parsed.eta,
            traceback=parsed.traceback,
            id=parsed.id,
            state=parsed.state,
            result=parsed.result,
        )
        res.raw_data = d
        return res
