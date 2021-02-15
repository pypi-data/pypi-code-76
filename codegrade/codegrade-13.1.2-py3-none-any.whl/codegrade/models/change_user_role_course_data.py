"""The module that defines the ``ChangeUserRoleCourseData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Type, Union

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..parsers import ParserFor, make_union
from ..utils import to_dict


@dataclass
class ChangeUserRoleCourseData_1:
    """Pass this data if you want to change the role of an existing member."""

    #: The id of the new role the user.
    role_id: "int"
    #: The id of the user of which you want to change the role.
    user_id: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "role_id",
                rqa.SimpleValue.int,
                doc="The id of the new role the user.",
            ),
            rqa.RequiredArgument(
                "user_id",
                rqa.SimpleValue.int,
                doc="The id of the user of which you want to change the role.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["role_id"] = to_dict(self.role_id)
        res["user_id"] = to_dict(self.user_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["ChangeUserRoleCourseData_1"], d: Dict[str, Any]
    ) -> "ChangeUserRoleCourseData_1":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            role_id=parsed.role_id,
            user_id=parsed.user_id,
        )
        res.raw_data = d
        return res


@dataclass
class ChangeUserRoleCourseData_1_2:
    """Pass this data if you want to enroll a new user"""

    #: The id of the new role the user.
    role_id: "int"
    #: The username of the user.
    username: "str"
    #: The id of the tenant of the user, this value will become required
    #: starting with release Nobel.2
    tenant_id: Maybe["str"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "role_id",
                rqa.SimpleValue.int,
                doc="The id of the new role the user.",
            ),
            rqa.RequiredArgument(
                "username",
                rqa.SimpleValue.str,
                doc="The username of the user.",
            ),
            rqa.OptionalArgument(
                "tenant_id",
                rqa.SimpleValue.str,
                doc=(
                    "The id of the tenant of the user, this value will become"
                    " required starting with release Nobel.2"
                ),
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        self.tenant_id = maybe_from_nullable(self.tenant_id)

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["role_id"] = to_dict(self.role_id)
        res["username"] = to_dict(self.username)
        if self.tenant_id.is_just:
            res["tenant_id"] = to_dict(self.tenant_id.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["ChangeUserRoleCourseData_1_2"], d: Dict[str, Any]
    ) -> "ChangeUserRoleCourseData_1_2":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            role_id=parsed.role_id,
            username=parsed.username,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res


ChangeUserRoleCourseData = Union[
    ChangeUserRoleCourseData_1,
    ChangeUserRoleCourseData_1_2,
]
ChangeUserRoleCourseDataParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(ChangeUserRoleCourseData_1),
        ParserFor.make(ChangeUserRoleCourseData_1_2),
    ),
)
