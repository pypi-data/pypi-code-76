"""The module that defines the ``FinalizedLTI1p1Provider`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from typing_extensions import Literal

from ..utils import to_dict
from .base_lti1p1_provider import BaseLTI1p1Provider


@dataclass
class FinalizedLTI1p1Provider(BaseLTI1p1Provider):
    """The JSON representation of a finalized provider."""

    #: This is a already finalized provider and thus is actively being used.
    finalized: "Literal[True]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseLTI1p1Provider.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "finalized",
                    rqa.LiteralBoolean(True),
                    doc=(
                        "This is a already finalized provider and thus is"
                        " actively being used."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["finalized"] = to_dict(self.finalized)
        res["version"] = to_dict(self.version)
        res["id"] = to_dict(self.id)
        res["lms"] = to_dict(self.lms)
        res["created_at"] = to_dict(self.created_at)
        res["intended_use"] = to_dict(self.intended_use)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["FinalizedLTI1p1Provider"], d: Dict[str, Any]
    ) -> "FinalizedLTI1p1Provider":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            finalized=parsed.finalized,
            version=parsed.version,
            id=parsed.id,
            lms=parsed.lms,
            created_at=parsed.created_at,
            intended_use=parsed.intended_use,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
