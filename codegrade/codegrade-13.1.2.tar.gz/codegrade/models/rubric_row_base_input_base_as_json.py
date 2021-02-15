"""The module that defines the ``RubricRowBaseInputBaseAsJSON`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .rubric_item_input_as_json import RubricItemInputAsJSON


@dataclass
class RubricRowBaseInputBaseAsJSON:
    """The required part of the input data for a rubric row."""

    #: The header of this row.
    header: "str"
    #: The description of this row.
    description: "str"
    #: The items in this row.
    items: "Sequence[RubricItemInputAsJSON]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "header",
                rqa.SimpleValue.str,
                doc="The header of this row.",
            ),
            rqa.RequiredArgument(
                "description",
                rqa.SimpleValue.str,
                doc="The description of this row.",
            ),
            rqa.RequiredArgument(
                "items",
                rqa.List(ParserFor.make(RubricItemInputAsJSON)),
                doc="The items in this row.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["header"] = to_dict(self.header)
        res["description"] = to_dict(self.description)
        res["items"] = to_dict(self.items)
        return res

    @classmethod
    def from_dict(
        cls: Type["RubricRowBaseInputBaseAsJSON"], d: Dict[str, Any]
    ) -> "RubricRowBaseInputBaseAsJSON":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            header=parsed.header,
            description=parsed.description,
            items=parsed.items,
        )
        res.raw_data = d
        return res
