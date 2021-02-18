"""The module that defines the ``RubricRowBase`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type, Union

import cg_request_args as rqa

from ..parsers import ParserFor, make_union
from ..utils import to_dict
from .rubric_description_type import RubricDescriptionType
from .rubric_item import RubricItem
from .rubric_lock_reason import RubricLockReason


@dataclass
class RubricRowBase:
    """The JSON representation of a rubric row."""

    #: The id of this row, used for updating
    id: "int"
    #: The header of this row.
    header: "str"
    #: The description of this row.
    description: "Optional[str]"
    #: The type of descriptions in this row.
    description_type: "RubricDescriptionType"
    #: The item in this row. The length will always be 1 for continuous rubric
    #: rows.
    items: "Sequence[RubricItem]"
    #: Is this row locked. If it is locked you cannot update it, nor can you
    #: manually select items in it.
    locked: "Union[RubricLockReason, bool]"
    #: The type of rubric row.
    type: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this row, used for updating",
            ),
            rqa.RequiredArgument(
                "header",
                rqa.SimpleValue.str,
                doc="The header of this row.",
            ),
            rqa.RequiredArgument(
                "description",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="The description of this row.",
            ),
            rqa.RequiredArgument(
                "description_type",
                rqa.EnumValue(RubricDescriptionType),
                doc="The type of descriptions in this row.",
            ),
            rqa.RequiredArgument(
                "items",
                rqa.List(ParserFor.make(RubricItem)),
                doc=(
                    "The item in this row. The length will always be 1 for"
                    " continuous rubric rows."
                ),
            ),
            rqa.RequiredArgument(
                "locked",
                make_union(
                    rqa.EnumValue(RubricLockReason), rqa.SimpleValue.bool
                ),
                doc=(
                    "Is this row locked. If it is locked you cannot update it,"
                    " nor can you manually select items in it."
                ),
            ),
            rqa.RequiredArgument(
                "type",
                rqa.SimpleValue.str,
                doc="The type of rubric row.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["header"] = to_dict(self.header)
        res["description"] = to_dict(self.description)
        res["description_type"] = to_dict(self.description_type)
        res["items"] = to_dict(self.items)
        res["locked"] = to_dict(self.locked)
        res["type"] = to_dict(self.type)
        return res

    @classmethod
    def from_dict(
        cls: Type["RubricRowBase"], d: Dict[str, Any]
    ) -> "RubricRowBase":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            header=parsed.header,
            description=parsed.description,
            description_type=parsed.description_type,
            items=parsed.items,
            locked=parsed.locked,
            type=parsed.type,
        )
        res.raw_data = d
        return res
