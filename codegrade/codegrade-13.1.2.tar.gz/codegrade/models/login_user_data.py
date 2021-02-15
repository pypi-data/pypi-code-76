"""The module that defines the ``LoginUserData`` model.

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
class LoginUserData_1:
    """The data required when you want to login"""

    #: The username of the user.
    username: "str"
    #: Your password
    password: "str"
    #: The id of the tenant of the user, this value will become required
    #: starting with release Nobel.2
    tenant_id: Maybe["str"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "username",
                rqa.SimpleValue.str,
                doc="The username of the user.",
            ),
            rqa.RequiredArgument(
                "password",
                rqa.SimpleValue.str,
                doc="Your password",
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
        res["username"] = to_dict(self.username)
        res["password"] = to_dict(self.password)
        if self.tenant_id.is_just:
            res["tenant_id"] = to_dict(self.tenant_id.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["LoginUserData_1"], d: Dict[str, Any]
    ) -> "LoginUserData_1":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            username=parsed.username,
            password=parsed.password,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res


@dataclass
class LoginUserData_1_2:
    """The data required when you want to impersonate a user"""

    #: The username of the user.
    username: "str"
    #: Your own password
    own_password: "str"
    #: The id of the tenant of the user, this value will become required
    #: starting with release Nobel.2
    tenant_id: Maybe["str"] = Nothing

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "username",
                rqa.SimpleValue.str,
                doc="The username of the user.",
            ),
            rqa.RequiredArgument(
                "own_password",
                rqa.SimpleValue.str,
                doc="Your own password",
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
        res["username"] = to_dict(self.username)
        res["own_password"] = to_dict(self.own_password)
        if self.tenant_id.is_just:
            res["tenant_id"] = to_dict(self.tenant_id.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["LoginUserData_1_2"], d: Dict[str, Any]
    ) -> "LoginUserData_1_2":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            username=parsed.username,
            own_password=parsed.own_password,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res


LoginUserData = Union[
    LoginUserData_1,
    LoginUserData_1_2,
]
LoginUserDataParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(LoginUserData_1),
        ParserFor.make(LoginUserData_1_2),
    ),
)
