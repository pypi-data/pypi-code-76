"""The module that defines the ``SiteSettingInput`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Optional,
    Sequence,
    Type,
    Union,
)

import cg_request_args as rqa
from typing_extensions import Literal

from ..parsers import ParserFor, make_union
from ..utils import to_dict


@dataclass
class AutoTestMaxTimeCommandSetting:
    """"""

    name: "Literal['AUTO_TEST_MAX_TIME_COMMAND']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_TIME_COMMAND"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestMaxTimeCommandSetting"], d: Dict[str, Any]
    ) -> "AutoTestMaxTimeCommandSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestHeartbeatIntervalSetting:
    """"""

    name: "Literal['AUTO_TEST_HEARTBEAT_INTERVAL']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_HEARTBEAT_INTERVAL"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestHeartbeatIntervalSetting"], d: Dict[str, Any]
    ) -> "AutoTestHeartbeatIntervalSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestHeartbeatMaxMissedSetting:
    """"""

    name: "Literal['AUTO_TEST_HEARTBEAT_MAX_MISSED']"
    value: "Optional[int]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_HEARTBEAT_MAX_MISSED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestHeartbeatMaxMissedSetting"], d: Dict[str, Any]
    ) -> "AutoTestHeartbeatMaxMissedSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxJobsPerRunnerSetting:
    """"""

    name: "Literal['AUTO_TEST_MAX_JOBS_PER_RUNNER']"
    value: "Optional[int]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_JOBS_PER_RUNNER"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestMaxJobsPerRunnerSetting"], d: Dict[str, Any]
    ) -> "AutoTestMaxJobsPerRunnerSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxConcurrentBatchRunsSetting:
    """"""

    name: "Literal['AUTO_TEST_MAX_CONCURRENT_BATCH_RUNS']"
    value: "Optional[int]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_CONCURRENT_BATCH_RUNS"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestMaxConcurrentBatchRunsSetting"], d: Dict[str, Any]
    ) -> "AutoTestMaxConcurrentBatchRunsSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestIoTestMessageSetting:
    """"""

    name: "Literal['AUTO_TEST_IO_TEST_MESSAGE']"
    value: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_IO_TEST_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestIoTestMessageSetting"], d: Dict[str, Any]
    ) -> "AutoTestIoTestMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestIoTestSubMessageSetting:
    """"""

    name: "Literal['AUTO_TEST_IO_TEST_SUB_MESSAGE']"
    value: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_IO_TEST_SUB_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestIoTestSubMessageSetting"], d: Dict[str, Any]
    ) -> "AutoTestIoTestSubMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestRunProgramMessageSetting:
    """"""

    name: "Literal['AUTO_TEST_RUN_PROGRAM_MESSAGE']"
    value: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_RUN_PROGRAM_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestRunProgramMessageSetting"], d: Dict[str, Any]
    ) -> "AutoTestRunProgramMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestCapturePointsMessageSetting:
    """"""

    name: "Literal['AUTO_TEST_CAPTURE_POINTS_MESSAGE']"
    value: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_CAPTURE_POINTS_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestCapturePointsMessageSetting"], d: Dict[str, Any]
    ) -> "AutoTestCapturePointsMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestCheckpointMessageSetting:
    """"""

    name: "Literal['AUTO_TEST_CHECKPOINT_MESSAGE']"
    value: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_CHECKPOINT_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestCheckpointMessageSetting"], d: Dict[str, Any]
    ) -> "AutoTestCheckpointMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestUnitTestMessageSetting:
    """"""

    name: "Literal['AUTO_TEST_UNIT_TEST_MESSAGE']"
    value: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_UNIT_TEST_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestUnitTestMessageSetting"], d: Dict[str, Any]
    ) -> "AutoTestUnitTestMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestCodeQualityMessageSetting:
    """"""

    name: "Literal['AUTO_TEST_CODE_QUALITY_MESSAGE']"
    value: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_CODE_QUALITY_MESSAGE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestCodeQualityMessageSetting"], d: Dict[str, Any]
    ) -> "AutoTestCodeQualityMessageSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class ExamLoginMaxLengthSetting:
    """"""

    name: "Literal['EXAM_LOGIN_MAX_LENGTH']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("EXAM_LOGIN_MAX_LENGTH"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["ExamLoginMaxLengthSetting"], d: Dict[str, Any]
    ) -> "ExamLoginMaxLengthSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class LoginTokenBeforeTimeSetting:
    """"""

    name: "Literal['LOGIN_TOKEN_BEFORE_TIME']"
    value: "Optional[Sequence[Union[int, str]]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("LOGIN_TOKEN_BEFORE_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    rqa.List(
                        make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                    )
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["LoginTokenBeforeTimeSetting"], d: Dict[str, Any]
    ) -> "LoginTokenBeforeTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MinPasswordScoreSetting:
    """"""

    name: "Literal['MIN_PASSWORD_SCORE']"
    value: "Optional[int]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MIN_PASSWORD_SCORE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["MinPasswordScoreSetting"], d: Dict[str, Any]
    ) -> "MinPasswordScoreSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class ResetTokenTimeSetting:
    """"""

    name: "Literal['RESET_TOKEN_TIME']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("RESET_TOKEN_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["ResetTokenTimeSetting"], d: Dict[str, Any]
    ) -> "ResetTokenTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class SettingTokenTimeSetting:
    """"""

    name: "Literal['SETTING_TOKEN_TIME']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("SETTING_TOKEN_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["SettingTokenTimeSetting"], d: Dict[str, Any]
    ) -> "SettingTokenTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class SiteEmailSetting:
    """"""

    name: "Literal['SITE_EMAIL']"
    value: "Optional[str]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("SITE_EMAIL"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.str),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["SiteEmailSetting"], d: Dict[str, Any]
    ) -> "SiteEmailSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxNumberOfFilesSetting:
    """"""

    name: "Literal['MAX_NUMBER_OF_FILES']"
    value: "Optional[int]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_NUMBER_OF_FILES"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["MaxNumberOfFilesSetting"], d: Dict[str, Any]
    ) -> "MaxNumberOfFilesSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxLargeUploadSizeSetting:
    """"""

    name: "Literal['MAX_LARGE_UPLOAD_SIZE']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_LARGE_UPLOAD_SIZE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["MaxLargeUploadSizeSetting"], d: Dict[str, Any]
    ) -> "MaxLargeUploadSizeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxNormalUploadSizeSetting:
    """"""

    name: "Literal['MAX_NORMAL_UPLOAD_SIZE']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_NORMAL_UPLOAD_SIZE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["MaxNormalUploadSizeSetting"], d: Dict[str, Any]
    ) -> "MaxNormalUploadSizeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxFileSizeSetting:
    """"""

    name: "Literal['MAX_FILE_SIZE']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_FILE_SIZE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["MaxFileSizeSetting"], d: Dict[str, Any]
    ) -> "MaxFileSizeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class JwtAccessTokenExpiresSetting:
    """"""

    name: "Literal['JWT_ACCESS_TOKEN_EXPIRES']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("JWT_ACCESS_TOKEN_EXPIRES"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["JwtAccessTokenExpiresSetting"], d: Dict[str, Any]
    ) -> "JwtAccessTokenExpiresSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxLinesSetting:
    """"""

    name: "Literal['MAX_LINES']"
    value: "Optional[int]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_LINES"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["MaxLinesSetting"], d: Dict[str, Any]
    ) -> "MaxLinesSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class NotificationPollTimeSetting:
    """"""

    name: "Literal['NOTIFICATION_POLL_TIME']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("NOTIFICATION_POLL_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["NotificationPollTimeSetting"], d: Dict[str, Any]
    ) -> "NotificationPollTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class ReleaseMessageMaxTimeSetting:
    """"""

    name: "Literal['RELEASE_MESSAGE_MAX_TIME']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("RELEASE_MESSAGE_MAX_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["ReleaseMessageMaxTimeSetting"], d: Dict[str, Any]
    ) -> "ReleaseMessageMaxTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class MaxPlagiarismMatchesSetting:
    """"""

    name: "Literal['MAX_PLAGIARISM_MATCHES']"
    value: "Optional[int]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("MAX_PLAGIARISM_MATCHES"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.int),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["MaxPlagiarismMatchesSetting"], d: Dict[str, Any]
    ) -> "MaxPlagiarismMatchesSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxGlobalSetupTimeSetting:
    """"""

    name: "Literal['AUTO_TEST_MAX_GLOBAL_SETUP_TIME']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_GLOBAL_SETUP_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestMaxGlobalSetupTimeSetting"], d: Dict[str, Any]
    ) -> "AutoTestMaxGlobalSetupTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestMaxPerStudentSetupTimeSetting:
    """"""

    name: "Literal['AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestMaxPerStudentSetupTimeSetting"], d: Dict[str, Any]
    ) -> "AutoTestMaxPerStudentSetupTimeSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class ServerTimeDiffToleranceSetting:
    """"""

    name: "Literal['SERVER_TIME_DIFF_TOLERANCE']"
    value: "Optional[Union[int, str]]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("SERVER_TIME_DIFF_TOLERANCE"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(
                    make_union(rqa.SimpleValue.int, rqa.SimpleValue.str)
                ),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["ServerTimeDiffToleranceSetting"], d: Dict[str, Any]
    ) -> "ServerTimeDiffToleranceSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class BlackboardZipUploadEnabledSetting:
    """"""

    name: "Literal['BLACKBOARD_ZIP_UPLOAD_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("BLACKBOARD_ZIP_UPLOAD_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["BlackboardZipUploadEnabledSetting"], d: Dict[str, Any]
    ) -> "BlackboardZipUploadEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class RubricsEnabledSetting:
    """"""

    name: "Literal['RUBRICS_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("RUBRICS_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["RubricsEnabledSetting"], d: Dict[str, Any]
    ) -> "RubricsEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutomaticLtiRoleEnabledSetting:
    """"""

    name: "Literal['AUTOMATIC_LTI_ROLE_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTOMATIC_LTI_ROLE_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutomaticLtiRoleEnabledSetting"], d: Dict[str, Any]
    ) -> "AutomaticLtiRoleEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class LtiEnabledSetting:
    """"""

    name: "Literal['LTI_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("LTI_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["LtiEnabledSetting"], d: Dict[str, Any]
    ) -> "LtiEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class LintersEnabledSetting:
    """"""

    name: "Literal['LINTERS_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("LINTERS_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["LintersEnabledSetting"], d: Dict[str, Any]
    ) -> "LintersEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class IncrementalRubricSubmissionEnabledSetting:
    """"""

    name: "Literal['INCREMENTAL_RUBRIC_SUBMISSION_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("INCREMENTAL_RUBRIC_SUBMISSION_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["IncrementalRubricSubmissionEnabledSetting"],
        d: Dict[str, Any],
    ) -> "IncrementalRubricSubmissionEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class RegisterEnabledSetting:
    """"""

    name: "Literal['REGISTER_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("REGISTER_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["RegisterEnabledSetting"], d: Dict[str, Any]
    ) -> "RegisterEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class GroupsEnabledSetting:
    """"""

    name: "Literal['GROUPS_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("GROUPS_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["GroupsEnabledSetting"], d: Dict[str, Any]
    ) -> "GroupsEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class AutoTestEnabledSetting:
    """"""

    name: "Literal['AUTO_TEST_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("AUTO_TEST_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["AutoTestEnabledSetting"], d: Dict[str, Any]
    ) -> "AutoTestEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class CourseRegisterEnabledSetting:
    """"""

    name: "Literal['COURSE_REGISTER_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("COURSE_REGISTER_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["CourseRegisterEnabledSetting"], d: Dict[str, Any]
    ) -> "CourseRegisterEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class RenderHtmlEnabledSetting:
    """"""

    name: "Literal['RENDER_HTML_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("RENDER_HTML_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["RenderHtmlEnabledSetting"], d: Dict[str, Any]
    ) -> "RenderHtmlEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class EmailStudentsEnabledSetting:
    """"""

    name: "Literal['EMAIL_STUDENTS_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("EMAIL_STUDENTS_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["EmailStudentsEnabledSetting"], d: Dict[str, Any]
    ) -> "EmailStudentsEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


@dataclass
class PeerFeedbackEnabledSetting:
    """"""

    name: "Literal['PEER_FEEDBACK_ENABLED']"
    value: "Optional[bool]"

    raw_data: Optional[Dict[str, Any]] = field(init=False, repr=False)

    data_parser: ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.StringEnum("PEER_FEEDBACK_ENABLED"),
                doc="",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> Dict[str, Any]:
        res = {}
        res["name"] = to_dict(self.name)
        res["value"] = to_dict(self.value)
        return res

    @classmethod
    def from_dict(
        cls: Type["PeerFeedbackEnabledSetting"], d: Dict[str, Any]
    ) -> "PeerFeedbackEnabledSetting":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res


SiteSettingInput = Union[
    AutoTestMaxTimeCommandSetting,
    AutoTestHeartbeatIntervalSetting,
    AutoTestHeartbeatMaxMissedSetting,
    AutoTestMaxJobsPerRunnerSetting,
    AutoTestMaxConcurrentBatchRunsSetting,
    AutoTestIoTestMessageSetting,
    AutoTestIoTestSubMessageSetting,
    AutoTestRunProgramMessageSetting,
    AutoTestCapturePointsMessageSetting,
    AutoTestCheckpointMessageSetting,
    AutoTestUnitTestMessageSetting,
    AutoTestCodeQualityMessageSetting,
    ExamLoginMaxLengthSetting,
    LoginTokenBeforeTimeSetting,
    MinPasswordScoreSetting,
    ResetTokenTimeSetting,
    SettingTokenTimeSetting,
    SiteEmailSetting,
    MaxNumberOfFilesSetting,
    MaxLargeUploadSizeSetting,
    MaxNormalUploadSizeSetting,
    MaxFileSizeSetting,
    JwtAccessTokenExpiresSetting,
    MaxLinesSetting,
    NotificationPollTimeSetting,
    ReleaseMessageMaxTimeSetting,
    MaxPlagiarismMatchesSetting,
    AutoTestMaxGlobalSetupTimeSetting,
    AutoTestMaxPerStudentSetupTimeSetting,
    ServerTimeDiffToleranceSetting,
    BlackboardZipUploadEnabledSetting,
    RubricsEnabledSetting,
    AutomaticLtiRoleEnabledSetting,
    LtiEnabledSetting,
    LintersEnabledSetting,
    IncrementalRubricSubmissionEnabledSetting,
    RegisterEnabledSetting,
    GroupsEnabledSetting,
    AutoTestEnabledSetting,
    CourseRegisterEnabledSetting,
    RenderHtmlEnabledSetting,
    EmailStudentsEnabledSetting,
    PeerFeedbackEnabledSetting,
]
SiteSettingInputParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(AutoTestMaxTimeCommandSetting),
        ParserFor.make(AutoTestHeartbeatIntervalSetting),
        ParserFor.make(AutoTestHeartbeatMaxMissedSetting),
        ParserFor.make(AutoTestMaxJobsPerRunnerSetting),
        ParserFor.make(AutoTestMaxConcurrentBatchRunsSetting),
        ParserFor.make(AutoTestIoTestMessageSetting),
        ParserFor.make(AutoTestIoTestSubMessageSetting),
        ParserFor.make(AutoTestRunProgramMessageSetting),
        ParserFor.make(AutoTestCapturePointsMessageSetting),
        ParserFor.make(AutoTestCheckpointMessageSetting),
        ParserFor.make(AutoTestUnitTestMessageSetting),
        ParserFor.make(AutoTestCodeQualityMessageSetting),
        ParserFor.make(ExamLoginMaxLengthSetting),
        ParserFor.make(LoginTokenBeforeTimeSetting),
        ParserFor.make(MinPasswordScoreSetting),
        ParserFor.make(ResetTokenTimeSetting),
        ParserFor.make(SettingTokenTimeSetting),
        ParserFor.make(SiteEmailSetting),
        ParserFor.make(MaxNumberOfFilesSetting),
        ParserFor.make(MaxLargeUploadSizeSetting),
        ParserFor.make(MaxNormalUploadSizeSetting),
        ParserFor.make(MaxFileSizeSetting),
        ParserFor.make(JwtAccessTokenExpiresSetting),
        ParserFor.make(MaxLinesSetting),
        ParserFor.make(NotificationPollTimeSetting),
        ParserFor.make(ReleaseMessageMaxTimeSetting),
        ParserFor.make(MaxPlagiarismMatchesSetting),
        ParserFor.make(AutoTestMaxGlobalSetupTimeSetting),
        ParserFor.make(AutoTestMaxPerStudentSetupTimeSetting),
        ParserFor.make(ServerTimeDiffToleranceSetting),
        ParserFor.make(BlackboardZipUploadEnabledSetting),
        ParserFor.make(RubricsEnabledSetting),
        ParserFor.make(AutomaticLtiRoleEnabledSetting),
        ParserFor.make(LtiEnabledSetting),
        ParserFor.make(LintersEnabledSetting),
        ParserFor.make(IncrementalRubricSubmissionEnabledSetting),
        ParserFor.make(RegisterEnabledSetting),
        ParserFor.make(GroupsEnabledSetting),
        ParserFor.make(AutoTestEnabledSetting),
        ParserFor.make(CourseRegisterEnabledSetting),
        ParserFor.make(RenderHtmlEnabledSetting),
        ParserFor.make(EmailStudentsEnabledSetting),
        ParserFor.make(PeerFeedbackEnabledSetting),
    ),
)
