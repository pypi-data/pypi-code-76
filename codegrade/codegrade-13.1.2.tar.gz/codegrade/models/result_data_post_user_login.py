"""The module that defines the ``ResultDataPostUserLogin`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..parsers import ParserFor
from ..utils import to_dict
from .extended_user import ExtendedUser


@dataclass
class ResultDataPostUserLogin:
    """When logging in this object will be given."""

    #: The user that was logged in.
    user: "ExtendedUser"
    #: A JWT token that can be used to do authenticated requests.
    access_token: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "user",
                ParserFor.make(ExtendedUser),
                doc="The user that was logged in.",
            ),
            rqa.RequiredArgument(
                "access_token",
                rqa.SimpleValue.str,
                doc=(
                    "A JWT token that can be used to do authenticated"
                    " requests."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["user"] = to_dict(self.user)
        res["access_token"] = to_dict(self.access_token)
        return res

    @classmethod
    def from_dict(
        cls: Type["ResultDataPostUserLogin"], d: Dict[str, Any]
    ) -> "ResultDataPostUserLogin":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            user=parsed.user,
            access_token=parsed.access_token,
        )
        res.raw_data = d
        return res
