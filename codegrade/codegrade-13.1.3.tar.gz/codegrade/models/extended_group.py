"""The module that defines the ``ExtendedGroup`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .group import Group
from .user_without_group import UserWithoutGroup


@dataclass
class ExtendedGroup(Group):
    """The group as extended JSON."""

    #: The virtual user connected to this course. It will not contain the
    #: `group` key as this would lead to an infinite recursion.
    virtual_user: "UserWithoutGroup"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: Group.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "virtual_user",
                    ParserFor.make(UserWithoutGroup),
                    doc=(
                        "The virtual user connected to this course. It will"
                        " not contain the `group` key as this would lead to an"
                        " infinite recursion."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["virtual_user"] = to_dict(self.virtual_user)
        res["id"] = to_dict(self.id)
        res["members"] = to_dict(self.members)
        res["name"] = to_dict(self.name)
        res["group_set_id"] = to_dict(self.group_set_id)
        res["created_at"] = to_dict(self.created_at)
        return res

    @classmethod
    def from_dict(
        cls: Type["ExtendedGroup"], d: Dict[str, Any]
    ) -> "ExtendedGroup":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            virtual_user=parsed.virtual_user,
            id=parsed.id,
            members=parsed.members,
            name=parsed.name,
            group_set_id=parsed.group_set_id,
            created_at=parsed.created_at,
        )
        res.raw_data = d
        return res
