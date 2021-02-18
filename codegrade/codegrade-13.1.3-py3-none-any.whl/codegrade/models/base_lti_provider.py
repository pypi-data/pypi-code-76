"""The module that defines the ``BaseLTIProvider`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import datetime
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class BaseLTIProvider:
    """The base JSON representation for an LTI 1.1 provider."""

    #: The id of this LTI provider.
    id: "str"
    #: The LMS that is connected as this LTI provider.
    lms: "str"
    #: The time this LTI provider was created.
    created_at: "datetime.datetime"
    #: Who will use this LTI provider.
    intended_use: "str"
    #: The id of the tenant that owns this provider.
    tenant_id: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "id",
                rqa.SimpleValue.str,
                doc="The id of this LTI provider.",
            ),
            rqa.RequiredArgument(
                "lms",
                rqa.SimpleValue.str,
                doc="The LMS that is connected as this LTI provider.",
            ),
            rqa.RequiredArgument(
                "created_at",
                rqa.RichValue.DateTime,
                doc="The time this LTI provider was created.",
            ),
            rqa.RequiredArgument(
                "intended_use",
                rqa.SimpleValue.str,
                doc="Who will use this LTI provider.",
            ),
            rqa.RequiredArgument(
                "tenant_id",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="The id of the tenant that owns this provider.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["id"] = to_dict(self.id)
        res["lms"] = to_dict(self.lms)
        res["created_at"] = to_dict(self.created_at)
        res["intended_use"] = to_dict(self.intended_use)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["BaseLTIProvider"], d: Dict[str, Any]
    ) -> "BaseLTIProvider":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            id=parsed.id,
            lms=parsed.lms,
            created_at=parsed.created_at,
            intended_use=parsed.intended_use,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
