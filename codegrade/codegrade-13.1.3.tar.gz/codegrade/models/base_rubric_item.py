"""The module that defines the ``BaseRubricItem`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class BaseRubricItem:
    """The base serialization of a rubric item."""

    #: The description of this item
    description: "str"
    #: The header of the item.
    header: "str"
    #: The amount of points a user gets when this item is selected.
    points: "float"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "description",
                rqa.SimpleValue.str,
                doc="The description of this item",
            ),
            rqa.RequiredArgument(
                "header",
                rqa.SimpleValue.str,
                doc="The header of the item.",
            ),
            rqa.RequiredArgument(
                "points",
                rqa.SimpleValue.float,
                doc=(
                    "The amount of points a user gets when this item is"
                    " selected."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["description"] = to_dict(self.description)
        res["header"] = to_dict(self.header)
        res["points"] = to_dict(self.points)
        return res

    @classmethod
    def from_dict(
        cls: Type["BaseRubricItem"], d: Dict[str, Any]
    ) -> "BaseRubricItem":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            description=parsed.description,
            header=parsed.header,
            points=parsed.points,
        )
        res.raw_data = d
        return res
