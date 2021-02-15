"""The module that defines the ``BaseLTI1p1Provider`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from typing_extensions import Literal

from ..utils import to_dict
from .base_lti_provider import BaseLTIProvider


@dataclass
class BaseLTI1p1Provider(BaseLTIProvider):
    """The base JSON representation of a LTI 1.1 provider."""

    #: The LTI version used.
    version: "Literal['lti1.1']"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseLTIProvider.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "version",
                    rqa.StringEnum("lti1.1"),
                    doc="The LTI version used.",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["version"] = to_dict(self.version)
        res["id"] = to_dict(self.id)
        res["lms"] = to_dict(self.lms)
        res["created_at"] = to_dict(self.created_at)
        res["intended_use"] = to_dict(self.intended_use)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["BaseLTI1p1Provider"], d: Dict[str, Any]
    ) -> "BaseLTI1p1Provider":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            version=parsed.version,
            id=parsed.id,
            lms=parsed.lms,
            created_at=parsed.created_at,
            intended_use=parsed.intended_use,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
