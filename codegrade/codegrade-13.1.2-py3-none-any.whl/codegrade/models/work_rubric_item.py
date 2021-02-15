"""The module that defines the ``WorkRubricItem`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict
from .rubric_item import RubricItem


@dataclass
class WorkRubricItem(RubricItem):
    """The connection between a submission and a rubric item."""

    #: The multiplier of this rubric item. This is especially useful for
    #: continuous rows, if a user achieved 50% of the points this will 0.5 for
    #: that rubric row.
    multiplier: "float"
    #: The amount of achieved points in this rubric item. This is simply the
    #: `points` field multiplied by the `multiplier` field.
    achieved_points: "float"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: RubricItem.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "multiplier",
                    rqa.SimpleValue.float,
                    doc=(
                        "The multiplier of this rubric item. This is"
                        " especially useful for continuous rows, if a user"
                        " achieved 50% of the points this will 0.5 for that"
                        " rubric row."
                    ),
                ),
                rqa.RequiredArgument(
                    "achieved_points",
                    rqa.SimpleValue.float,
                    doc=(
                        "The amount of achieved points in this rubric item."
                        " This is simply the `points` field multiplied by the"
                        " `multiplier` field."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["multiplier"] = to_dict(self.multiplier)
        res["achieved_points"] = to_dict(self.achieved_points)
        res["id"] = to_dict(self.id)
        res["description"] = to_dict(self.description)
        res["header"] = to_dict(self.header)
        res["points"] = to_dict(self.points)
        return res

    @classmethod
    def from_dict(
        cls: Type["WorkRubricItem"], d: Dict[str, Any]
    ) -> "WorkRubricItem":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            multiplier=parsed.multiplier,
            achieved_points=parsed.achieved_points,
            id=parsed.id,
            description=parsed.description,
            header=parsed.header,
            points=parsed.points,
        )
        res.raw_data = d
        return res
