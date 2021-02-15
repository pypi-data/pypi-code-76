"""The module that defines the ``UserInput`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..utils import to_dict


@dataclass
class UserInput:
    """The user you want to add to the group"""

    #: The username of the user.
    username: "str"
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
        if self.tenant_id.is_just:
            res["tenant_id"] = to_dict(self.tenant_id.value)
        return res

    @classmethod
    def from_dict(cls: Type["UserInput"], d: Dict[str, Any]) -> "UserInput":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            username=parsed.username,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
