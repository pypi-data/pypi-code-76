"""The module that defines the ``NonFinalizedLTI1p1Provider`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa
from typing_extensions import Literal

from ..utils import to_dict
from .base_lti1p1_provider import BaseLTI1p1Provider


@dataclass
class NonFinalizedLTI1p1Provider(BaseLTI1p1Provider):
    """The JSON representation of a non finalized provider."""

    #: This is a non finalized provider, so it cannot yet be used for launches.
    finalized: "Literal[False]"
    #: If you have the permission to edit this provider this will be a key with
    #: which you can do that.
    edit_secret: "Optional[str]"
    #: The consumer key used to connect the provider to an LMS.
    lms_consumer_key: "str"
    #: The shared secret used to connect the provider to an LMS.
    lms_consumer_secret: "str"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: BaseLTI1p1Provider.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "finalized",
                    rqa.LiteralBoolean(False),
                    doc=(
                        "This is a non finalized provider, so it cannot yet be"
                        " used for launches."
                    ),
                ),
                rqa.RequiredArgument(
                    "edit_secret",
                    rqa.Nullable(rqa.SimpleValue.str),
                    doc=(
                        "If you have the permission to edit this provider this"
                        " will be a key with which you can do that."
                    ),
                ),
                rqa.RequiredArgument(
                    "lms_consumer_key",
                    rqa.SimpleValue.str,
                    doc=(
                        "The consumer key used to connect the provider to an"
                        " LMS."
                    ),
                ),
                rqa.RequiredArgument(
                    "lms_consumer_secret",
                    rqa.SimpleValue.str,
                    doc=(
                        "The shared secret used to connect the provider to an"
                        " LMS."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["finalized"] = to_dict(self.finalized)
        res["edit_secret"] = to_dict(self.edit_secret)
        res["lms_consumer_key"] = to_dict(self.lms_consumer_key)
        res["lms_consumer_secret"] = to_dict(self.lms_consumer_secret)
        res["version"] = to_dict(self.version)
        res["id"] = to_dict(self.id)
        res["lms"] = to_dict(self.lms)
        res["created_at"] = to_dict(self.created_at)
        res["intended_use"] = to_dict(self.intended_use)
        res["tenant_id"] = to_dict(self.tenant_id)
        return res

    @classmethod
    def from_dict(
        cls: Type["NonFinalizedLTI1p1Provider"], d: Dict[str, Any]
    ) -> "NonFinalizedLTI1p1Provider":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            finalized=parsed.finalized,
            edit_secret=parsed.edit_secret,
            lms_consumer_key=parsed.lms_consumer_key,
            lms_consumer_secret=parsed.lms_consumer_secret,
            version=parsed.version,
            id=parsed.id,
            lms=parsed.lms,
            created_at=parsed.created_at,
            intended_use=parsed.intended_use,
            tenant_id=parsed.tenant_id,
        )
        res.raw_data = d
        return res
