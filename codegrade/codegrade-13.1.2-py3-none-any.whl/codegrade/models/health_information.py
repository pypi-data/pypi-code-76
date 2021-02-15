"""The module that defines the ``HealthInformation`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class HealthInformation:
    """Information about the health of this instance."""

    #: Always true.
    application: "bool"
    #: Is the database ok?
    database: "bool"
    #: Is the upload storage system ok?
    uploads: "bool"
    #: Can the broker be reached?
    broker: "bool"
    #: Is the mirror upload storage system ok?
    mirror_uploads: "bool"
    #: Is the temporary directory on this server ok?
    temp_dir: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "application",
                rqa.SimpleValue.bool,
                doc="Always true.",
            ),
            rqa.RequiredArgument(
                "database",
                rqa.SimpleValue.bool,
                doc="Is the database ok?",
            ),
            rqa.RequiredArgument(
                "uploads",
                rqa.SimpleValue.bool,
                doc="Is the upload storage system ok?",
            ),
            rqa.RequiredArgument(
                "broker",
                rqa.SimpleValue.bool,
                doc="Can the broker be reached?",
            ),
            rqa.RequiredArgument(
                "mirror_uploads",
                rqa.SimpleValue.bool,
                doc="Is the mirror upload storage system ok?",
            ),
            rqa.RequiredArgument(
                "temp_dir",
                rqa.SimpleValue.bool,
                doc="Is the temporary directory on this server ok?",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["application"] = to_dict(self.application)
        res["database"] = to_dict(self.database)
        res["uploads"] = to_dict(self.uploads)
        res["broker"] = to_dict(self.broker)
        res["mirror_uploads"] = to_dict(self.mirror_uploads)
        res["temp_dir"] = to_dict(self.temp_dir)
        return res

    @classmethod
    def from_dict(
        cls: Type["HealthInformation"], d: Dict[str, Any]
    ) -> "HealthInformation":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            application=parsed.application,
            database=parsed.database,
            uploads=parsed.uploads,
            broker=parsed.broker,
            mirror_uploads=parsed.mirror_uploads,
            temp_dir=parsed.temp_dir,
        )
        res.raw_data = d
        return res
