# flake8:noqa:E402
import asyncio
import logging
from typing import Any, Awaitable, Callable, Optional

from nonebot import get_driver
from nonebot.adapters.cqhttp.message import Message

from ..config import DefaultConfig
from ..poly import CQHttp, Event
from . import default_config
from .log import logger
from .sched import Scheduler

if Scheduler:
    scheduler = Scheduler()
else:
    scheduler = None


class NoneBot(CQHttp):
    def __init__(self, config_object: Optional[Any] = None):
        super().__init__()

        config_object = config_object or default_config
        config_dict = {
            k: getattr(config_object, k)
            for k in dir(config_object)
            if k.isupper() and not k.startswith("_")
        }

        self.config = DefaultConfig.parse_obj(config_dict)
        logger.debug(f"Loaded configurations: {config_dict}")

        self.logger.setLevel(logging.DEBUG if self.config.DEBUG else logging.INFO)

        from .message import handle_message
        from .notice_request import handle_notice_or_request

        @self.on_message
        async def _msg_handler(selfevent: Event):
            asyncio.create_task(handle_message(self, selfevent))

        @self.on_notice
        async def _not_handler(selfevent: Event):
            asyncio.create_task(handle_notice_or_request(self, selfevent))

        @self.on_request
        async def _req_handler(selfevent: Event):
            asyncio.create_task(handle_notice_or_request(self, selfevent))


_bot: Optional[NoneBot] = None


def init(config: Optional[Any] = None, enable_scheduler: bool = True):
    global _bot
    _bot = NoneBot(config)

    if enable_scheduler and scheduler and not scheduler.running:
        scheduler.configure(_bot.config.APSCHEDULER_CONFIG)
        scheduler.start()
        logger.info("Scheduler started")

    return _bot


def get_bot() -> NoneBot:
    """
    Get the NoneBot instance.

    The result is ensured to be not None, otherwise an exception will
    be raised.

    :raise ValueError: instance not initialized
    """
    if _bot is None:
        raise ValueError("NoneBot instance has not been initialized")
    return _bot


def on_startup(func: Callable[[], Awaitable[None]]) -> Callable[[], Awaitable[None]]:
    """
    Decorator to register a function as startup callback.
    """
    return get_driver().on_startup(func)


def on_websocket_connect(
    func: Callable[[Event], Awaitable[None]]
) -> Callable[[], Awaitable[None]]:
    """
    Decorator to register a function as websocket connect callback.

    Only work with CQHTTP v4.14+.
    """
    return get_bot().on_meta_event("lifecycle.connect")(func)  # type: ignore


from .command import CommandGroup, CommandSession
from .exceptions import CQHttpError
from .helpers import context_id
from .message import Message, MessageSegment, message_preprocessor
from .natural_language import IntentCommand, NLPResult, NLPSession
from .notice_request import NoticeSession, RequestSession
from .plugin import (get_loaded_plugins, load_builtin_plugins, load_plugin,
                     load_plugins, on_command, on_natural_language, on_notice,
                     on_request)

__all__ = [
    "NoneBot",
    "scheduler",
    "init",
    "get_bot",
    "on_startup",
    "on_websocket_connect",
    "CQHttpError",
    "load_plugin",
    "load_plugins",
    "load_builtin_plugins",
    "get_loaded_plugins",
    "message_preprocessor",
    "Message",
    "MessageSegment",
    "on_command",
    "CommandSession",
    "CommandGroup",
    "on_natural_language",
    "NLPSession",
    "NLPResult",
    "IntentCommand",
    "on_notice",
    "NoticeSession",
    "on_request",
    "RequestSession",
    "context_id",
]
