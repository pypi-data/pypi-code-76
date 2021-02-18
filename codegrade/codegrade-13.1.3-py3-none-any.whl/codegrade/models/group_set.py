"""The module that defines the ``GroupSet`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class GroupSet:
    """The way this class will be represented in JSON."""

    #: The id of this group set.
    id: "int"
    #: The minimum size a group should be before it can submit work.
    minimum_size: "int"
    #: The maximum size a group can be.
    maximum_size: "int"
    #: The ids of the assignments connected to this group set.
    assignment_ids: "Sequence[int]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this group set.",
            ),
            rqa.RequiredArgument(
                "minimum_size",
                rqa.SimpleValue.int,
                doc=(
                    "The minimum size a group should be before it can submit"
                    " work."
                ),
            ),
            rqa.RequiredArgument(
                "maximum_size",
                rqa.SimpleValue.int,
                doc="The maximum size a group can be.",
            ),
            rqa.RequiredArgument(
                "assignment_ids",
                rqa.List(rqa.SimpleValue.int),
                doc="The ids of the assignments connected to this group set.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["minimum_size"] = to_dict(self.minimum_size)
        res["maximum_size"] = to_dict(self.maximum_size)
        res["assignment_ids"] = to_dict(self.assignment_ids)
        return res

    @classmethod
    def from_dict(cls: Type["GroupSet"], d: Dict[str, Any]) -> "GroupSet":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            minimum_size=parsed.minimum_size,
            maximum_size=parsed.maximum_size,
            assignment_ids=parsed.assignment_ids,
        )
        res.raw_data = d
        return res
