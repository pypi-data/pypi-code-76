"""The module that defines the ``CreateLTIData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Type, Union

import cg_request_args as rqa
from typing_extensions import Literal

from ..parsers import ParserFor, make_union
from ..utils import to_dict


@dataclass
class CreateLTIData_1:
    """"""

    #: The id of the tenant that will use this LMS
    tenant_id: "str"
    #: The LMS that will be used for this connection
    lms: "Literal['Canvas', 'Blackboard', 'Sakai', 'Open edX', 'Moodle', 'BrightSpace']"
    #: Use LTI 1.1
    lti_version: "Literal['lti1.1']"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "tenant_id",
                rqa.SimpleValue.str,
                doc="The id of the tenant that will use this LMS",
            ),
            rqa.RequiredArgument(
                "lms",
                rqa.StringEnum(
                    "Canvas",
                    "Blackboard",
                    "Sakai",
                    "Open edX",
                    "Moodle",
                    "BrightSpace",
                ),
                doc="The LMS that will be used for this connection",
            ),
            rqa.RequiredArgument(
                "lti_version",
                rqa.StringEnum("lti1.1"),
                doc="Use LTI 1.1",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["tenant_id"] = to_dict(self.tenant_id)
        res["lms"] = to_dict(self.lms)
        res["lti_version"] = to_dict(self.lti_version)
        return res

    @classmethod
    def from_dict(
        cls: Type["CreateLTIData_1"], d: Dict[str, Any]
    ) -> "CreateLTIData_1":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            tenant_id=parsed.tenant_id,
            lms=parsed.lms,
            lti_version=parsed.lti_version,
        )
        res.raw_data = d
        return res


@dataclass
class CreateLTIData_1_2:
    """"""

    #: The id of the tenant that will use this LMS
    tenant_id: "str"
    #: The iss of the new provider
    iss: "str"
    #: The LMS that will be used for this connection
    lms: "Literal['Canvas', 'Blackboard', 'Moodle', 'Brightspace']"
    #: Use LTI 1.3
    lti_version: "Literal['lti1.3']" = "lti1.3"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "tenant_id",
                rqa.SimpleValue.str,
                doc="The id of the tenant that will use this LMS",
            ),
            rqa.RequiredArgument(
                "iss",
                rqa.SimpleValue.str,
                doc="The iss of the new provider",
            ),
            rqa.RequiredArgument(
                "lms",
                rqa.StringEnum(
                    "Canvas", "Blackboard", "Moodle", "Brightspace"
                ),
                doc="The LMS that will be used for this connection",
            ),
            rqa.DefaultArgument(
                "lti_version",
                rqa.StringEnum("lti1.3"),
                doc="Use LTI 1.3",
                default=lambda: "lti1.3",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["tenant_id"] = to_dict(self.tenant_id)
        res["iss"] = to_dict(self.iss)
        res["lms"] = to_dict(self.lms)
        res["lti_version"] = to_dict(self.lti_version)
        return res

    @classmethod
    def from_dict(
        cls: Type["CreateLTIData_1_2"], d: Dict[str, Any]
    ) -> "CreateLTIData_1_2":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            tenant_id=parsed.tenant_id,
            iss=parsed.iss,
            lms=parsed.lms,
            lti_version=parsed.lti_version,
        )
        res.raw_data = d
        return res


CreateLTIData = Union[
    CreateLTIData_1,
    CreateLTIData_1_2,
]
CreateLTIDataParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(CreateLTIData_1),
        ParserFor.make(CreateLTIData_1_2),
    ),
)
