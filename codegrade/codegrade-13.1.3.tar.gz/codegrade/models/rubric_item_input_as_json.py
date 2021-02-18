"""The module that defines the ``RubricItemInputAsJSON`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..utils import to_dict
from .base_rubric_item import BaseRubricItem


@dataclass
class RubricItemInputAsJSON(BaseRubricItem):
    """The JSON needed to update a rubric item."""

    #: The id of this rubric item. Pass this to update an existing rubric item,
    #: omit if you want to create a new item.
    id: Maybe["int"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseRubricItem.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.OptionalArgument(
                    "id",
                    rqa.SimpleValue.int,
                    doc=(
                        "The id of this rubric item. Pass this to update an"
                        " existing rubric item, omit if you want to create a"
                        " new item."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.id = maybe_from_nullable(self.id)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["description"] = to_dict(self.description)
        res["header"] = to_dict(self.header)
        res["points"] = to_dict(self.points)
        if self.id.is_just:
            res["id"] = to_dict(self.id.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["RubricItemInputAsJSON"], d: Dict[str, Any]
    ) -> "RubricItemInputAsJSON":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            description=parsed.description,
            header=parsed.header,
            points=parsed.points,
            id=parsed.id,
        )
        res.raw_data = d
        return res
