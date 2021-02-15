"""The module that defines the ``ColumnRange`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class ColumnRange:
    """A column range."""

    #: The column the comment starts (inclusive), one indexed.
    start: "int"
    #: The column the comment ends (inclusive), one indexed. If it is `null`
    #: the comments spans till the end of the line.
    end: "Optional[int]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "start",
                rqa.SimpleValue.int,
                doc="The column the comment starts (inclusive), one indexed.",
            ),
            rqa.RequiredArgument(
                "end",
                rqa.Nullable(rqa.SimpleValue.int),
                doc=(
                    "The column the comment ends (inclusive), one indexed. If"
                    " it is `null` the comments spans till the end of the"
                    " line."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["start"] = to_dict(self.start)
        res["end"] = to_dict(self.end)
        return res

    @classmethod
    def from_dict(
        cls: Type["ColumnRange"], d: Dict[str, Any]
    ) -> "ColumnRange":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            start=parsed.start,
            end=parsed.end,
        )
        res.raw_data = d
        return res
