"""The module that defines the ``AutoTestRun`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from typing_extensions import Literal

from ..utils import to_dict


@dataclass
class AutoTestRun:
    """The run as JSON."""

    #: The id of this run.
    id: "int"
    #: The moment the run was created.
    created_at: "datetime.datetime"
    #: The state it is in. This is only kept for backwards compatibility
    #: reasons, it will always be "running".
    state: "Literal['running']"
    #: Also not used anymore, will always be `false`.
    is_continuous: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.int,
                doc="The id of this run.",
            ),
            rqa.RequiredArgument(
                "created_at",
                rqa.RichValue.DateTime,
                doc="The moment the run was created.",
            ),
            rqa.RequiredArgument(
                "state",
                rqa.StringEnum("running"),
                doc=(
                    "The state it is in. This is only kept for backwards"
                    ' compatibility reasons, it will always be "running".'
                ),
            ),
            rqa.RequiredArgument(
                "is_continuous",
                rqa.SimpleValue.bool,
                doc="Also not used anymore, will always be `false`.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["created_at"] = to_dict(self.created_at)
        res["state"] = to_dict(self.state)
        res["is_continuous"] = to_dict(self.is_continuous)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestRun"], d: Dict[str, Any]
    ) -> "AutoTestRun":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            created_at=parsed.created_at,
            state=parsed.state,
            is_continuous=parsed.is_continuous,
        )
        res.raw_data = d
        return res
