"""The module that defines the ``RubricItem`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict
from .base_rubric_item import BaseRubricItem


@dataclass
class RubricItem(BaseRubricItem):
    """The JSON representation of a rubric item."""

    #: The id of this rubric item.
    id: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseRubricItem.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "id",
                    rqa.SimpleValue.int,
                    doc="The id of this rubric item.",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["description"] = to_dict(self.description)
        res["header"] = to_dict(self.header)
        res["points"] = to_dict(self.points)
        return res

    @classmethod
    def from_dict(cls: Type["RubricItem"], d: Dict[str, Any]) -> "RubricItem":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            description=parsed.description,
            header=parsed.header,
            points=parsed.points,
        )
        res.raw_data = d
        return res
