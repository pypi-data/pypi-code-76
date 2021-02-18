"""The module that defines the ``TenantCourseStatistics`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class TenantCourseStatistics:
    """Information about the amount of courses a tenant has."""

    #: The total amount of courses of this tenant.
    total: "int"
    #: The amount of "active" courses this tenant has. An active course is a
    #: course in which a student has created a submission within the last 31
    #: days.
    active: "int"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "total",
                rqa.SimpleValue.int,
                doc="The total amount of courses of this tenant.",
            ),
            rqa.RequiredArgument(
                "active",
                rqa.SimpleValue.int,
                doc=(
                    'The amount of "active" courses this tenant has. An active'
                    " course is a course in which a student has created a"
                    " submission within the last 31 days."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["total"] = to_dict(self.total)
        res["active"] = to_dict(self.active)
        return res

    @classmethod
    def from_dict(
        cls: Type["TenantCourseStatistics"], d: Dict[str, Any]
    ) -> "TenantCourseStatistics":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            total=parsed.total,
            active=parsed.active,
        )
        res.raw_data = d
        return res
