"""The module that defines the ``BaseLTI1p3Provider`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from typing_extensions import Literal

from ..parsers import ParserFor
from ..utils import to_dict
from .base_lti_provider import BaseLTIProvider
from .lms_capabilities import LMSCapabilities


@dataclass
class BaseLTI1p3Provider(BaseLTIProvider):
    """The base representation of an LTI 1.3 provider."""

    #: The capabilities of this LMS
    capabilities: "LMSCapabilities"
    #: The LTI version used.
    version: "Literal['lti1.3']"
    #: The iss configured for this provider.
    iss: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseLTIProvider.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "capabilities",
                    ParserFor.make(LMSCapabilities),
                    doc="The capabilities of this LMS",
                ),
                rqa.RequiredArgument(
                    "version",
                    rqa.StringEnum("lti1.3"),
                    doc="The LTI version used.",
                ),
                rqa.RequiredArgument(
                    "iss",
                    rqa.SimpleValue.str,
                    doc="The iss configured for this provider.",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["capabilities"] = to_dict(self.capabilities)
        res["version"] = to_dict(self.version)
        res["iss"] = to_dict(self.iss)
        res["id"] = to_dict(self.id)
        res["lms"] = to_dict(self.lms)
        res["created_at"] = to_dict(self.created_at)
        res["intended_use"] = to_dict(self.intended_use)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["BaseLTI1p3Provider"], d: Dict[str, Any]
    ) -> "BaseLTI1p3Provider":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            capabilities=parsed.capabilities,
            version=parsed.version,
            iss=parsed.iss,
            id=parsed.id,
            lms=parsed.lms,
            created_at=parsed.created_at,
            intended_use=parsed.intended_use,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
