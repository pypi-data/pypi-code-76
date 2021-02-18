"""The module that defines the ``LegacyFeatures`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class LegacyFeatures:
    """The legacy features of CodeGrade.

    Please don't use this object, but instead check for enabled settings.
    """

    #: See settings.
    automatic_lti_role: "bool"
    #: See settings.
    auto_test: "bool"
    #: See settings.
    blackboard_zip_upload: "bool"
    #: See settings.
    course_register: "bool"
    #: See settings.
    email_students: "bool"
    #: See settings.
    groups: "bool"
    #: See settings.
    incremental_rubric_submission: "bool"
    #: See settings.
    lti: "bool"
    #: See settings.
    peer_feedback: "bool"
    #: See settings.
    register: "bool"
    #: See settings.
    render_html: "bool"
    #: See settings.
    rubrics: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "AUTOMATIC_LTI_ROLE",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "AUTO_TEST",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "BLACKBOARD_ZIP_UPLOAD",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "COURSE_REGISTER",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "EMAIL_STUDENTS",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "GROUPS",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "INCREMENTAL_RUBRIC_SUBMISSION",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "LTI",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "PEER_FEEDBACK",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "REGISTER",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "RENDER_HTML",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
            rqa.RequiredArgument(
                "RUBRICS",
                rqa.SimpleValue.bool,
                doc="See settings.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["AUTOMATIC_LTI_ROLE"] = to_dict(self.automatic_lti_role)
        res["AUTO_TEST"] = to_dict(self.auto_test)
        res["BLACKBOARD_ZIP_UPLOAD"] = to_dict(self.blackboard_zip_upload)
        res["COURSE_REGISTER"] = to_dict(self.course_register)
        res["EMAIL_STUDENTS"] = to_dict(self.email_students)
        res["GROUPS"] = to_dict(self.groups)
        res["INCREMENTAL_RUBRIC_SUBMISSION"] = to_dict(
            self.incremental_rubric_submission
        )
        res["LTI"] = to_dict(self.lti)
        res["PEER_FEEDBACK"] = to_dict(self.peer_feedback)
        res["REGISTER"] = to_dict(self.register)
        res["RENDER_HTML"] = to_dict(self.render_html)
        res["RUBRICS"] = to_dict(self.rubrics)
        return res

    @classmethod
    def from_dict(
        cls: Type["LegacyFeatures"], d: Dict[str, Any]
    ) -> "LegacyFeatures":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            automatic_lti_role=parsed.AUTOMATIC_LTI_ROLE,
            auto_test=parsed.AUTO_TEST,
            blackboard_zip_upload=parsed.BLACKBOARD_ZIP_UPLOAD,
            course_register=parsed.COURSE_REGISTER,
            email_students=parsed.EMAIL_STUDENTS,
            groups=parsed.GROUPS,
            incremental_rubric_submission=parsed.INCREMENTAL_RUBRIC_SUBMISSION,
            lti=parsed.LTI,
            peer_feedback=parsed.PEER_FEEDBACK,
            register=parsed.REGISTER,
            render_html=parsed.RENDER_HTML,
            rubrics=parsed.RUBRICS,
        )
        res.raw_data = d
        return res
