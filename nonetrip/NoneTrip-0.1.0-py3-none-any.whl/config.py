from datetime import timedelta
from typing import Any, Dict, Iterable, Optional, Pattern, Set, Union

from nonebot import get_driver
from nonebot.config import Config
from pydantic import BaseModel, Extra

from nonetrip.comp.typing import Expression_T

NoneBotConfig: Config = get_driver().config


class DefaultConfig(BaseModel):
    class Config:
        extra = Extra.allow

    API_ROOT: str = ""
    ACCESS_TOKEN: str = ""
    SECRET: str = ""
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    DEBUG: bool = True

    SUPERUSERS: Set[int] = set()
    NICKNAME: Union[str, Iterable[str]] = ""

    COMMAND_START: Iterable[Union[str, Pattern]] = {"/", "!", "／", "！"}
    COMMAND_SEP: Iterable[Union[str, Pattern]] = {"/", "."}

    SESSION_EXPIRE_TIMEOUT: Optional[timedelta] = timedelta(minutes=5)
    SESSION_RUN_TIMEOUT: Optional[timedelta] = None
    SESSION_RUNNING_EXPRESSION: Expression_T = "您有命令正在执行，请稍后再试"

    SHORT_MESSAGE_MAX_LENGTH: int = 50

    DEFAULT_VALIDATION_FAILURE_EXPRESSION: Expression_T = "您的输入不符合要求，请重新输入"
    MAX_VALIDATION_FAILURES: int = 3
    TOO_MANY_VALIDATION_FAILURES_EXPRESSION: Expression_T = "您输入错误太多次啦，如需重试，请重新触发本功能"

    SESSION_CANCEL_EXPRESSION: Expression_T = "好的"

    APSCHEDULER_CONFIG: Dict[str, Any] = {"apscheduler.timezone": "Asia/Shanghai"}
