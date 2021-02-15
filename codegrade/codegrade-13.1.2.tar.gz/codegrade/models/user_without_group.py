"""The module that defines the ``UserWithoutGroup`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class UserWithoutGroup:
    """The JSON representation of a user without the `group` property."""

    #: The is the id of this user
    id: "int"
    #: The fullname of the user. This might contain a first and last name,
    #: however this is not guaranteed.
    name: "str"
    #: The username of this user.
    username: "str"
    #: Is this user a test student.
    is_test_student: "bool"
    #: The tenant of the user
    tenant_id: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The is the id of this user",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc=(
                    "The fullname of the user. This might contain a first and"
                    " last name, however this is not guaranteed."
                ),
            ),
            rqa.RequiredArgument(
                "username",
                rqa.SimpleValue.str,
                doc="The username of this user.",
            ),
            rqa.RequiredArgument(
                "is_test_student",
                rqa.SimpleValue.bool,
                doc="Is this user a test student.",
            ),
            rqa.RequiredArgument(
                "tenant_id",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="The tenant of the user",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["name"] = to_dict(self.name)
        res["username"] = to_dict(self.username)
        res["is_test_student"] = to_dict(self.is_test_student)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["UserWithoutGroup"], d: Dict[str, Any]
    ) -> "UserWithoutGroup":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            name=parsed.name,
            username=parsed.username,
            is_test_student=parsed.is_test_student,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
