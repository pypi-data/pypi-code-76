"""The module that defines the ``AllSiteSettings`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Optional, Type

import cg_request_args as rqa

from ..utils import to_dict
from .frontend_site_settings import FrontendSiteSettings


@dataclass
class AllSiteSettings(FrontendSiteSettings):
    """The JSON representation of all options."""

    #: The amount of time there can be between two heartbeats of a runner.
    #: Changing this to a lower value might cause some runners to crash.
    auto_test_heartbeat_interval: "float"
    #: The max amount of heartbeats that we may miss from a runner before we
    #: kill it and start a new one.
    auto_test_heartbeat_max_missed: "int"
    #: This value determines the amount of runners we request for a single
    #: assignment. The amount of runners requested is equal to the amount of
    #: students not yet started divided by this value.
    auto_test_max_jobs_per_runner: "int"
    #: The maximum amount of batch AutoTest runs we will do at a time. AutoTest
    #: batch runs are runs that are done after the deadline for configurations
    #: that have hidden tests. Increasing this variable might cause heavy
    #: server load.
    auto_test_max_concurrent_batch_runs: "int"
    #: The minimum strength passwords by users should have. The higher this
    #: value the stronger the password should be. When increasing the strength
    #: all users with too weak passwords will be shown a warning on the next
    #: login.
    min_password_score: "int"
    #: The amount of time a reset token is valid. You should not increase this
    #: value too much as users might be not be too careful with these tokens.
    #: Increasing this value will allow **all** existing tokens to live longer.
    reset_token_time: "float"
    #: The amount of time the link send in notification emails to change the
    #: notification preferences works to actually change the notifications.
    setting_token_time: "float"
    #: The maximum amount of files and directories allowed in a single archive.
    max_number_of_files: "int"
    #: The maximum size of uploaded files that are mostly uploaded by "trusted"
    #: users. Examples of these kind of files include AutoTest fixtures and
    #: plagiarism base code.
    max_large_upload_size: "int"
    #: The maximum total size of uploaded files that are uploaded by normal
    #: users. This is also the maximum total size of submissions. Increasing
    #: this size might cause a hosting costs to increase.
    max_normal_upload_size: "int"
    #: The maximum size of a single file uploaded by normal users. This limit
    #: is really here to prevent users from uploading extremely large files
    #: which can't really be downloaded/shown anyway.
    max_file_size: "int"
    #: The time a login session is valid. After this amount of time a user will
    #: always need to re-authenticate.
    jwt_access_token_expires: "float"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: FrontendSiteSettings.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "AUTO_TEST_HEARTBEAT_INTERVAL",
                    rqa.SimpleValue.float,
                    doc=(
                        "The amount of time there can be between two"
                        " heartbeats of a runner. Changing this to a lower"
                        " value might cause some runners to crash."
                    ),
                ),
                rqa.RequiredArgument(
                    "AUTO_TEST_HEARTBEAT_MAX_MISSED",
                    rqa.SimpleValue.int,
                    doc=(
                        "The max amount of heartbeats that we may miss from a"
                        " runner before we kill it and start a new one."
                    ),
                ),
                rqa.RequiredArgument(
                    "AUTO_TEST_MAX_JOBS_PER_RUNNER",
                    rqa.SimpleValue.int,
                    doc=(
                        "This value determines the amount of runners we"
                        " request for a single assignment. The amount of"
                        " runners requested is equal to the amount of students"
                        " not yet started divided by this value."
                    ),
                ),
                rqa.RequiredArgument(
                    "AUTO_TEST_MAX_CONCURRENT_BATCH_RUNS",
                    rqa.SimpleValue.int,
                    doc=(
                        "The maximum amount of batch AutoTest runs we will do"
                        " at a time. AutoTest batch runs are runs that are"
                        " done after the deadline for configurations that have"
                        " hidden tests. Increasing this variable might cause"
                        " heavy server load."
                    ),
                ),
                rqa.RequiredArgument(
                    "MIN_PASSWORD_SCORE",
                    rqa.SimpleValue.int,
                    doc=(
                        "The minimum strength passwords by users should have."
                        " The higher this value the stronger the password"
                        " should be. When increasing the strength all users"
                        " with too weak passwords will be shown a warning on"
                        " the next login."
                    ),
                ),
                rqa.RequiredArgument(
                    "RESET_TOKEN_TIME",
                    rqa.SimpleValue.float,
                    doc=(
                        "The amount of time a reset token is valid. You should"
                        " not increase this value too much as users might be"
                        " not be too careful with these tokens. Increasing"
                        " this value will allow **all** existing tokens to"
                        " live longer."
                    ),
                ),
                rqa.RequiredArgument(
                    "SETTING_TOKEN_TIME",
                    rqa.SimpleValue.float,
                    doc=(
                        "The amount of time the link send in notification"
                        " emails to change the notification preferences works"
                        " to actually change the notifications."
                    ),
                ),
                rqa.RequiredArgument(
                    "MAX_NUMBER_OF_FILES",
                    rqa.SimpleValue.int,
                    doc=(
                        "The maximum amount of files and directories allowed"
                        " in a single archive."
                    ),
                ),
                rqa.RequiredArgument(
                    "MAX_LARGE_UPLOAD_SIZE",
                    rqa.SimpleValue.int,
                    doc=(
                        "The maximum size of uploaded files that are mostly"
                        ' uploaded by "trusted" users. Examples of these kind'
                        " of files include AutoTest fixtures and plagiarism"
                        " base code."
                    ),
                ),
                rqa.RequiredArgument(
                    "MAX_NORMAL_UPLOAD_SIZE",
                    rqa.SimpleValue.int,
                    doc=(
                        "The maximum total size of uploaded files that are"
                        " uploaded by normal users. This is also the maximum"
                        " total size of submissions. Increasing this size"
                        " might cause a hosting costs to increase."
                    ),
                ),
                rqa.RequiredArgument(
                    "MAX_FILE_SIZE",
                    rqa.SimpleValue.int,
                    doc=(
                        "The maximum size of a single file uploaded by normal"
                        " users. This limit is really here to prevent users"
                        " from uploading extremely large files which can't"
                        " really be downloaded/shown anyway."
                    ),
                ),
                rqa.RequiredArgument(
                    "JWT_ACCESS_TOKEN_EXPIRES",
                    rqa.SimpleValue.float,
                    doc=(
                        "The time a login session is valid. After this amount"
                        " of time a user will always need to re-authenticate."
                    ),
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["AUTO_TEST_HEARTBEAT_INTERVAL"] = to_dict(
            self.auto_test_heartbeat_interval
        )
        res["AUTO_TEST_HEARTBEAT_MAX_MISSED"] = to_dict(
            self.auto_test_heartbeat_max_missed
        )
        res["AUTO_TEST_MAX_JOBS_PER_RUNNER"] = to_dict(
            self.auto_test_max_jobs_per_runner
        )
        res["AUTO_TEST_MAX_CONCURRENT_BATCH_RUNS"] = to_dict(
            self.auto_test_max_concurrent_batch_runs
        )
        res["MIN_PASSWORD_SCORE"] = to_dict(self.min_password_score)
        res["RESET_TOKEN_TIME"] = to_dict(self.reset_token_time)
        res["SETTING_TOKEN_TIME"] = to_dict(self.setting_token_time)
        res["MAX_NUMBER_OF_FILES"] = to_dict(self.max_number_of_files)
        res["MAX_LARGE_UPLOAD_SIZE"] = to_dict(self.max_large_upload_size)
        res["MAX_NORMAL_UPLOAD_SIZE"] = to_dict(self.max_normal_upload_size)
        res["MAX_FILE_SIZE"] = to_dict(self.max_file_size)
        res["JWT_ACCESS_TOKEN_EXPIRES"] = to_dict(
            self.jwt_access_token_expires
        )
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
        cls: Type["AllSiteSettings"], d: Dict[str, Any]
    ) -> "AllSiteSettings":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            auto_test_heartbeat_interval=parsed.AUTO_TEST_HEARTBEAT_INTERVAL,
            auto_test_heartbeat_max_missed=parsed.AUTO_TEST_HEARTBEAT_MAX_MISSED,
            auto_test_max_jobs_per_runner=parsed.AUTO_TEST_MAX_JOBS_PER_RUNNER,
            auto_test_max_concurrent_batch_runs=parsed.AUTO_TEST_MAX_CONCURRENT_BATCH_RUNS,
            min_password_score=parsed.MIN_PASSWORD_SCORE,
            reset_token_time=parsed.RESET_TOKEN_TIME,
            setting_token_time=parsed.SETTING_TOKEN_TIME,
            max_number_of_files=parsed.MAX_NUMBER_OF_FILES,
            max_large_upload_size=parsed.MAX_LARGE_UPLOAD_SIZE,
            max_normal_upload_size=parsed.MAX_NORMAL_UPLOAD_SIZE,
            max_file_size=parsed.MAX_FILE_SIZE,
            jwt_access_token_expires=parsed.JWT_ACCESS_TOKEN_EXPIRES,
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
