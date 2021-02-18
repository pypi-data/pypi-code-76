"""The module that defines the ``Group`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .user_without_group import UserWithoutGroup


@dataclass
class Group:
    """The group as JSON."""

    #: The id of this gropu
    id: "int"
    #: The members of this group.
    members: "Sequence[UserWithoutGroup]"
    #: The name of this group.
    name: "str"
    #: The id of the group set that this group is connected to.
    group_set_id: "int"
    #: The datetime this group was created.
    created_at: "datetime.datetime"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this gropu",
            ),
            rqa.RequiredArgument(
                "members",
                rqa.List(ParserFor.make(UserWithoutGroup)),
                doc="The members of this group.",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="The name of this group.",
            ),
            rqa.RequiredArgument(
                "group_set_id",
                rqa.SimpleValue.int,
                doc="The id of the group set that this group is connected to.",
            ),
            rqa.RequiredArgument(
                "created_at",
                rqa.RichValue.DateTime,
                doc="The datetime this group was created.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["members"] = to_dict(self.members)
        res["name"] = to_dict(self.name)
        res["group_set_id"] = to_dict(self.group_set_id)
        res["created_at"] = to_dict(self.created_at)
        return res

    @classmethod
    def from_dict(cls: Type["Group"], d: Dict[str, Any]) -> "Group":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            members=parsed.members,
            name=parsed.name,
            group_set_id=parsed.group_set_id,
            created_at=parsed.created_at,
        )
        res.raw_data = d
        return res
