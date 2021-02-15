"""The module that defines the ``FrontendSiteSettings`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Sequence, Type

import cg_request_args as rqa

from ..utils import to_dict


@dataclass
class FrontendSiteSettings:
    """The JSON representation of options visible to all users."""

    #: The default amount of time a step/substep in AutoTest can run. This can
    #: be overridden by the teacher.
    auto_test_max_time_command: "float"
    #: Default message for IO Test steps of an AutoTest.
    auto_test_io_test_message: "str"
    #: Default message for IO Test sub-steps of an AutoTest.
    auto_test_io_test_sub_message: "str"
    #: Default message for Run Program steps of an AutoTest.
    auto_test_run_program_message: "str"
    #: Default message for Capture Points steps of an AutoTest.
    auto_test_capture_points_message: "str"
    #: Default message for Checkpoint steps of an AutoTest.
    auto_test_checkpoint_message: "str"
    #: Default message for Unit Test steps of an AutoTest.
    auto_test_unit_test_message: "str"
    #: Default message for Code Quality steps of an AutoTest.
    auto_test_code_quality_message: "str"
    #: The maximum time-delta an exam may take. Increasing this value also
    #: increases the maximum amount of time the login tokens send via email are
    #: valid. Therefore, you should make this too long.
    exam_login_max_length: "float"
    #: This determines how long before the exam we will send the login emails
    #: to the students (only when enabled of course).
    login_token_before_time: "Sequence[float]"
    #: The email shown to users as the email of CodeGrade.
    site_email: "str"
    #: The maximum amount of lines that we should in render in one go. If a
    #: file contains more lines than this we will show a warning asking the
    #: user what to do.
    max_lines: "int"
    #: The amount of time to wait between two consecutive polls to see if a
    #: user has new notifications. Setting this value too low will cause
    #: unnecessary stres on the server.
    notification_poll_time: "float"
    #: What is the maximum amount of time after a release a message should be
    #: shown on the HomeGrid. **Note**: this is the amount of time after the
    #: release, not after this instance has been upgraded to this release.
    release_message_max_time: "float"
    #: The maximum amount of matches of a plagiarism run that we will store. If
    #: there are more matches than this they will be discarded.
    max_plagiarism_matches: "int"
    #: The maximum amount of time that the global setup script in AutoTest may
    #: take. If it takes longer than this it will be killed and the run will
    #: fail.
    auto_test_max_global_setup_time: "float"
    #: The maximum amount of time that the per student setup script in AutoTest
    #: may take. If it takes longer than this it will be killed and the result
    #: of the student will be in the state "timed-out"
    auto_test_max_per_student_setup_time: "float"
    #: The maximum amount of difference between the server time and the local
    #: time before we consider the local time to be out of sync with our
    #: servers.
    server_time_diff_tolerance: "float"
    #: If enabled teachers are allowed to bulk upload submissions (and create
    #: users) using a zip file in a format created by Blackboard.
    blackboard_zip_upload_enabled: "bool"
    #: If enabled teachers can use rubrics on CodeGrade. Disabling this feature
    #: will not delete existing rubrics.
    rubrics_enabled: "bool"
    #: Currently unused
    automatic_lti_role_enabled: "bool"
    #: Should LTI be enabled.
    lti_enabled: "bool"
    #: Should linters be enabled
    linters_enabled: "bool"
    #: Should rubrics be submitted incrementally, so if a user selects a item
    #: should this be automatically be submitted to the server, or should it
    #: only be possible to submit a complete rubric at once. This feature is
    #: useless if rubrics is not set to true.
    incremental_rubric_submission_enabled: "bool"
    #: Should it be possible to register on the website. This makes it possible
    #: for any body to register an account on the website.
    register_enabled: "bool"
    #: Should group assignments be enabled.
    groups_enabled: "bool"
    #: Should auto test be enabled.
    auto_test_enabled: "bool"
    #: Should it be possible for teachers to create links that users can use to
    #: register in a course. Links to enroll can be created even if this
    #: feature is disabled.
    course_register_enabled: "bool"
    #: Should it be possible to render html files within CodeGrade. This opens
    #: up more attack surfaces as it is now possible by design for students to
    #: run javascript. This is all done in a sandboxed iframe but still.
    render_html_enabled: "bool"
    #: Should it be possible to email students.
    email_students_enabled: "bool"
    #: Should peer feedback be enabled.
    peer_feedback_enabled: "bool"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "AUTO_TEST_MAX_TIME_COMMAND",
                rqa.SimpleValue.float,
                doc=(
                    "The default amount of time a step/substep in AutoTest can"
                    " run. This can be overridden by the teacher."
                ),
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_IO_TEST_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for IO Test steps of an AutoTest.",
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_IO_TEST_SUB_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for IO Test sub-steps of an AutoTest.",
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_RUN_PROGRAM_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Run Program steps of an AutoTest.",
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_CAPTURE_POINTS_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Capture Points steps of an AutoTest.",
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_CHECKPOINT_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Checkpoint steps of an AutoTest.",
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_UNIT_TEST_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Unit Test steps of an AutoTest.",
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_CODE_QUALITY_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Code Quality steps of an AutoTest.",
            ),
            rqa.RequiredArgument(
                "EXAM_LOGIN_MAX_LENGTH",
                rqa.SimpleValue.float,
                doc=(
                    "The maximum time-delta an exam may take. Increasing this"
                    " value also increases the maximum amount of time the"
                    " login tokens send via email are valid. Therefore, you"
                    " should make this too long."
                ),
            ),
            rqa.RequiredArgument(
                "LOGIN_TOKEN_BEFORE_TIME",
                rqa.List(rqa.SimpleValue.float),
                doc=(
                    "This determines how long before the exam we will send the"
                    " login emails to the students (only when enabled of"
                    " course)."
                ),
            ),
            rqa.RequiredArgument(
                "SITE_EMAIL",
                rqa.SimpleValue.str,
                doc="The email shown to users as the email of CodeGrade.",
            ),
            rqa.RequiredArgument(
                "MAX_LINES",
                rqa.SimpleValue.int,
                doc=(
                    "The maximum amount of lines that we should in render in"
                    " one go. If a file contains more lines than this we will"
                    " show a warning asking the user what to do."
                ),
            ),
            rqa.RequiredArgument(
                "NOTIFICATION_POLL_TIME",
                rqa.SimpleValue.float,
                doc=(
                    "The amount of time to wait between two consecutive polls"
                    " to see if a user has new notifications. Setting this"
                    " value too low will cause unnecessary stres on the"
                    " server."
                ),
            ),
            rqa.RequiredArgument(
                "RELEASE_MESSAGE_MAX_TIME",
                rqa.SimpleValue.float,
                doc=(
                    "What is the maximum amount of time after a release a"
                    " message should be shown on the HomeGrid. **Note**: this"
                    " is the amount of time after the release, not after this"
                    " instance has been upgraded to this release."
                ),
            ),
            rqa.RequiredArgument(
                "MAX_PLAGIARISM_MATCHES",
                rqa.SimpleValue.int,
                doc=(
                    "The maximum amount of matches of a plagiarism run that we"
                    " will store. If there are more matches than this they"
                    " will be discarded."
                ),
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_MAX_GLOBAL_SETUP_TIME",
                rqa.SimpleValue.float,
                doc=(
                    "The maximum amount of time that the global setup script"
                    " in AutoTest may take. If it takes longer than this it"
                    " will be killed and the run will fail."
                ),
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME",
                rqa.SimpleValue.float,
                doc=(
                    "The maximum amount of time that the per student setup"
                    " script in AutoTest may take. If it takes longer than"
                    " this it will be killed and the result of the student"
                    ' will be in the state "timed-out"'
                ),
            ),
            rqa.RequiredArgument(
                "SERVER_TIME_DIFF_TOLERANCE",
                rqa.SimpleValue.float,
                doc=(
                    "The maximum amount of difference between the server time"
                    " and the local time before we consider the local time to"
                    " be out of sync with our servers."
                ),
            ),
            rqa.RequiredArgument(
                "BLACKBOARD_ZIP_UPLOAD_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "If enabled teachers are allowed to bulk upload"
                    " submissions (and create users) using a zip file in a"
                    " format created by Blackboard."
                ),
            ),
            rqa.RequiredArgument(
                "RUBRICS_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "If enabled teachers can use rubrics on CodeGrade."
                    " Disabling this feature will not delete existing rubrics."
                ),
            ),
            rqa.RequiredArgument(
                "AUTOMATIC_LTI_ROLE_ENABLED",
                rqa.SimpleValue.bool,
                doc="Currently unused",
            ),
            rqa.RequiredArgument(
                "LTI_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should LTI be enabled.",
            ),
            rqa.RequiredArgument(
                "LINTERS_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should linters be enabled",
            ),
            rqa.RequiredArgument(
                "INCREMENTAL_RUBRIC_SUBMISSION_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should rubrics be submitted incrementally, so if a user"
                    " selects a item should this be automatically be submitted"
                    " to the server, or should it only be possible to submit a"
                    " complete rubric at once. This feature is useless if"
                    " rubrics is not set to true."
                ),
            ),
            rqa.RequiredArgument(
                "REGISTER_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should it be possible to register on the website. This"
                    " makes it possible for any body to register an account on"
                    " the website."
                ),
            ),
            rqa.RequiredArgument(
                "GROUPS_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should group assignments be enabled.",
            ),
            rqa.RequiredArgument(
                "AUTO_TEST_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should auto test be enabled.",
            ),
            rqa.RequiredArgument(
                "COURSE_REGISTER_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should it be possible for teachers to create links that"
                    " users can use to register in a course. Links to enroll"
                    " can be created even if this feature is disabled."
                ),
            ),
            rqa.RequiredArgument(
                "RENDER_HTML_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should it be possible to render html files within"
                    " CodeGrade. This opens up more attack surfaces as it is"
                    " now possible by design for students to run javascript."
                    " This is all done in a sandboxed iframe but still."
                ),
            ),
            rqa.RequiredArgument(
                "EMAIL_STUDENTS_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should it be possible to email students.",
            ),
            rqa.RequiredArgument(
                "PEER_FEEDBACK_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should peer feedback be enabled.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["AUTO_TEST_MAX_TIME_COMMAND"] = to_dict(
            self.auto_test_max_time_command
        )
        res["AUTO_TEST_IO_TEST_MESSAGE"] = to_dict(
            self.auto_test_io_test_message
        )
        res["AUTO_TEST_IO_TEST_SUB_MESSAGE"] = to_dict(
            self.auto_test_io_test_sub_message
        )
        res["AUTO_TEST_RUN_PROGRAM_MESSAGE"] = to_dict(
            self.auto_test_run_program_message
        )
        res["AUTO_TEST_CAPTURE_POINTS_MESSAGE"] = to_dict(
            self.auto_test_capture_points_message
        )
        res["AUTO_TEST_CHECKPOINT_MESSAGE"] = to_dict(
            self.auto_test_checkpoint_message
        )
        res["AUTO_TEST_UNIT_TEST_MESSAGE"] = to_dict(
            self.auto_test_unit_test_message
        )
        res["AUTO_TEST_CODE_QUALITY_MESSAGE"] = to_dict(
            self.auto_test_code_quality_message
        )
        res["EXAM_LOGIN_MAX_LENGTH"] = to_dict(self.exam_login_max_length)
        res["LOGIN_TOKEN_BEFORE_TIME"] = to_dict(self.login_token_before_time)
        res["SITE_EMAIL"] = to_dict(self.site_email)
        res["MAX_LINES"] = to_dict(self.max_lines)
        res["NOTIFICATION_POLL_TIME"] = to_dict(self.notification_poll_time)
        res["RELEASE_MESSAGE_MAX_TIME"] = to_dict(
            self.release_message_max_time
        )
        res["MAX_PLAGIARISM_MATCHES"] = to_dict(self.max_plagiarism_matches)
        res["AUTO_TEST_MAX_GLOBAL_SETUP_TIME"] = to_dict(
            self.auto_test_max_global_setup_time
        )
        res["AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME"] = to_dict(
            self.auto_test_max_per_student_setup_time
        )
        res["SERVER_TIME_DIFF_TOLERANCE"] = to_dict(
            self.server_time_diff_tolerance
        )
        res["BLACKBOARD_ZIP_UPLOAD_ENABLED"] = to_dict(
            self.blackboard_zip_upload_enabled
        )
        res["RUBRICS_ENABLED"] = to_dict(self.rubrics_enabled)
        res["AUTOMATIC_LTI_ROLE_ENABLED"] = to_dict(
            self.automatic_lti_role_enabled
        )
        res["LTI_ENABLED"] = to_dict(self.lti_enabled)
        res["LINTERS_ENABLED"] = to_dict(self.linters_enabled)
        res["INCREMENTAL_RUBRIC_SUBMISSION_ENABLED"] = to_dict(
            self.incremental_rubric_submission_enabled
        )
        res["REGISTER_ENABLED"] = to_dict(self.register_enabled)
        res["GROUPS_ENABLED"] = to_dict(self.groups_enabled)
        res["AUTO_TEST_ENABLED"] = to_dict(self.auto_test_enabled)
        res["COURSE_REGISTER_ENABLED"] = to_dict(self.course_register_enabled)
        res["RENDER_HTML_ENABLED"] = to_dict(self.render_html_enabled)
        res["EMAIL_STUDENTS_ENABLED"] = to_dict(self.email_students_enabled)
        res["PEER_FEEDBACK_ENABLED"] = to_dict(self.peer_feedback_enabled)
        return res

    @classmethod
    def from_dict(
        cls: Type["FrontendSiteSettings"], d: Dict[str, Any]
    ) -> "FrontendSiteSettings":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            auto_test_max_time_command=parsed.AUTO_TEST_MAX_TIME_COMMAND,
            auto_test_io_test_message=parsed.AUTO_TEST_IO_TEST_MESSAGE,
            auto_test_io_test_sub_message=parsed.AUTO_TEST_IO_TEST_SUB_MESSAGE,
            auto_test_run_program_message=parsed.AUTO_TEST_RUN_PROGRAM_MESSAGE,
            auto_test_capture_points_message=parsed.AUTO_TEST_CAPTURE_POINTS_MESSAGE,
            auto_test_checkpoint_message=parsed.AUTO_TEST_CHECKPOINT_MESSAGE,
            auto_test_unit_test_message=parsed.AUTO_TEST_UNIT_TEST_MESSAGE,
            auto_test_code_quality_message=parsed.AUTO_TEST_CODE_QUALITY_MESSAGE,
            exam_login_max_length=parsed.EXAM_LOGIN_MAX_LENGTH,
            login_token_before_time=parsed.LOGIN_TOKEN_BEFORE_TIME,
            site_email=parsed.SITE_EMAIL,
            max_lines=parsed.MAX_LINES,
            notification_poll_time=parsed.NOTIFICATION_POLL_TIME,
            release_message_max_time=parsed.RELEASE_MESSAGE_MAX_TIME,
            max_plagiarism_matches=parsed.MAX_PLAGIARISM_MATCHES,
            auto_test_max_global_setup_time=parsed.AUTO_TEST_MAX_GLOBAL_SETUP_TIME,
            auto_test_max_per_student_setup_time=parsed.AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME,
            server_time_diff_tolerance=parsed.SERVER_TIME_DIFF_TOLERANCE,
            blackboard_zip_upload_enabled=parsed.BLACKBOARD_ZIP_UPLOAD_ENABLED,
            rubrics_enabled=parsed.RUBRICS_ENABLED,
            automatic_lti_role_enabled=parsed.AUTOMATIC_LTI_ROLE_ENABLED,
            lti_enabled=parsed.LTI_ENABLED,
            linters_enabled=parsed.LINTERS_ENABLED,
            incremental_rubric_submission_enabled=parsed.INCREMENTAL_RUBRIC_SUBMISSION_ENABLED,
            register_enabled=parsed.REGISTER_ENABLED,
            groups_enabled=parsed.GROUPS_ENABLED,
            auto_test_enabled=parsed.AUTO_TEST_ENABLED,
            course_register_enabled=parsed.COURSE_REGISTER_ENABLED,
            render_html_enabled=parsed.RENDER_HTML_ENABLED,
            email_students_enabled=parsed.EMAIL_STUDENTS_ENABLED,
            peer_feedback_enabled=parsed.PEER_FEEDBACK_ENABLED,
        )
        res.raw_data = d
        return res
