"""The module that defines the ``User`` model.

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
class User(UserWithoutGroup):
    """The JSON representation of a user."""

    #: If this user is a wrapper user for a group this will contain this group,
    #: otherwise it will be `null`.
    group: "Optional[Group]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: UserWithoutGroup.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "group",
                    rqa.Nullable(ParserFor.make(Group)),
                    doc=(
                        "If this user is a wrapper user for a group this will"
                        " contain this group, otherwise it will be `null`."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["group"] = to_dict(self.group)
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["username"] = to_dict(self.username)
        res["is_test_student"] = to_dict(self.is_test_student)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(cls: Type["User"], d: Dict[str, Any]) -> "User":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            group=parsed.group,
            id=parsed.id,
            name=parsed.name,
            username=parsed.username,
            is_test_student=parsed.is_test_student,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
