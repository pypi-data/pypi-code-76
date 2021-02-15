"""The module that defines the ``RegisterUserData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class RegisterUserData:
    """"""

    #: Username to register.
    username: "str"
    #: Password of the new user.
    password: "str"
    #: Email address of the new user.
    email: "str"
    #: Full name of the new user.
    name: "str"
    #: Id of the tenant to register the new user with.
    tenant_id: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "username",
                rqa.SimpleValue.str,
                doc="Username to register.",
            ),
            rqa.RequiredArgument(
                "password",
                rqa.SimpleValue.str,
                doc="Password of the new user.",
            ),
            rqa.RequiredArgument(
                "email",
                rqa.SimpleValue.str,
                doc="Email address of the new user.",
            ),
            rqa.RequiredArgument(
                "name",
                rqa.SimpleValue.str,
                doc="Full name of the new user.",
            ),
            rqa.RequiredArgument(
                "tenant_id",
                rqa.SimpleValue.str,
                doc="Id of the tenant to register the new user with.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["username"] = to_dict(self.username)
        res["password"] = to_dict(self.password)
        res["email"] = to_dict(self.email)
        res["name"] = to_dict(self.name)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["RegisterUserData"], d: Dict[str, Any]
    ) -> "RegisterUserData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            username=parsed.username,
            password=parsed.password,
            email=parsed.email,
            name=parsed.name,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
