"""Baseclasses for services using asyncio as eventloop"""
from typing import Union, MutableMapping, Any, Coroutine, Optional
from pathlib import Path
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import tempfile
import logging
import functools

import signal as posixsignal
import asyncio
import toml

from datastreamcorelib.abstract import ZMQSocketType, ZMQSocketDescription
from datastreamcorelib.utils import create_heartbeat_message


from .zmqwrappers import PubSubManager, pubsubmanager_factory
from .compat import cast_task

LOGGER = logging.getLogger(__name__)
EXCEPTION_EXITCODE = 200
SIGNALS_HOOKED = False


# See https://github.com/python/mypy/issues/5374 why the typing ignore
@dataclass  # type: ignore
class BaseService(ABC):
    """Baseclass for services using asyncio as eventloop"""

    disable_signals_hook: bool = field(init=False, default=False)
    _exitcode: Union[None, int] = field(init=False, default=None)
    _quitevent: asyncio.Event = field(init=False, default_factory=asyncio.Event, repr=False)

    @abstractmethod
    async def setup(self) -> None:
        """Called once by the run method before wating for exitcode to be set"""
        raise NotImplementedError()

    @abstractmethod
    async def teardown(self) -> None:
        """Called once by the run method before exiting"""
        raise NotImplementedError()

    @abstractmethod
    def reload(self) -> None:
        """Called whenever the service is told to reload (usually via SIGHUP), setup might want to call this"""
        raise NotImplementedError()

    def quit(self, exitcode: int = 0) -> None:
        """set the exitcode which as side-effect will tell the run method to do teardown and finally exit"""
        LOGGER.debug("called with code={}".format(exitcode))
        self._exitcode = exitcode
        self._quitevent.set()

    def hook_signals(self) -> None:
        """Hook handlers for signals and the default exception handler"""
        global SIGNALS_HOOKED  # pylint: disable=W0603
        if self.disable_signals_hook:
            LOGGER.info("Signal hooking disabled by property")
            return
        if SIGNALS_HOOKED:
            LOGGER.warning("Already hooked")
            return
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(self.default_exception_handler)
        loop.add_signal_handler(posixsignal.SIGINT, self.quit)
        loop.add_signal_handler(posixsignal.SIGTERM, self.quit)
        try:
            loop.add_signal_handler(posixsignal.SIGHUP, self.reload)
        except AttributeError:
            # Windows does not implement all signals
            pass
        SIGNALS_HOOKED = True

    def default_exception_handler(self, loop: asyncio.AbstractEventLoop, context: MutableMapping[str, Any]) -> None:
        """Default exception handler, logs the exception and quits (forcefully)"""
        msg = context.get("exception", context["message"])
        if isinstance(msg, Exception):
            LOGGER.exception("Unhandled in loop {}".format(loop), exc_info=msg)
        else:
            LOGGER.error("Called with context message {} in loop {}".format(msg, loop))
        # Make sure we get killed if quit hangs...
        BaseService.set_exit_alarm()
        # Call quit with the defined exit code
        self.quit(EXCEPTION_EXITCODE)

    @classmethod
    def set_exit_alarm(cls, timeout: int = 2) -> bool:
        """Clears handlers from alarm and sets an alarm signal for hard exit on timeout

        returns False if alarm could not be set. Yes, it can only take full integer seconds"""
        try:
            # Try to make sure alarm is not handled and set alarm to make sure teardown doesn't hang
            loop = asyncio.get_event_loop()
            loop.remove_signal_handler(posixsignal.SIGALRM)
            posixsignal.signal(posixsignal.SIGALRM, posixsignal.SIG_DFL)
            posixsignal.alarm(timeout)
            return True
        except AttributeError:
            # Windows does not implement all signals
            return False

    @classmethod
    def clear_exit_alarm(cls) -> bool:
        """Clear pending alarm"""
        try:
            posixsignal.signal(posixsignal.SIGALRM, posixsignal.SIG_DFL)
            posixsignal.alarm(0)
            return True
        except AttributeError:
            # Windows does not implement all signals
            return False

    async def run(self) -> int:
        """Main entrypoint, should be called with asyncio.get_event_loop().run_until_complete()"""
        await self.setup()
        await self._quitevent.wait()
        if self._exitcode is None:
            LOGGER.error("Got quitevent but exitcode is not set")
            self._exitcode = 1
        # Try to make sure teardown does not hang
        BaseService.set_exit_alarm()
        await self.teardown()
        return self._exitcode


@dataclass
class SimpleServiceMixin:
    """Mixin for a bit of automagics for heartbeats, config loading etc"""

    configpath: Path
    psmgr: PubSubManager = field(init=False, default_factory=pubsubmanager_factory)
    config: MutableMapping[str, Any] = field(init=False, default_factory=dict)
    _tasks: MutableMapping[str, "asyncio.Task[Any]"] = field(init=False, default_factory=dict)

    def create_task(self, coro: Coroutine[Any, Any, Any], *, name: Optional[str] = None) -> "asyncio.Task[Any]":
        """Helper to wrap asyncios create_task so that we always handle the exception and track long-running tasks"""
        task = asyncio.get_event_loop().create_task(coro)
        if name:
            if name in self._tasks:
                raise ValueError(f"name {name} is already tracked")
        else:
            name = f"Task-{id(task):02x}"

        task = cast_task(task)
        try:
            task.set_name(name)
        except AttributeError:
            # Ignore the missing method in py36 and add the get_name wrapper
            task.get_name = functools.partial(lambda retname: retname, name)  # type: ignore

        def report_error_remove_tracking(task: "asyncio.Task[Any]") -> None:
            """done callback to bubble up errors and remove tracking"""
            # Remove from tracking (we monkeypatched get_name above)
            task = cast_task(task)
            name = task.get_name()
            del self._tasks[name]
            # Bubble up any exceptions
            try:
                exc = task.exception()
                if exc:
                    LOGGER.error("Task {} raised exception {}".format(task, exc))
                    raise exc
            except asyncio.CancelledError:
                LOGGER.error("Task {} did not handle cancellation".format(task))

        self._tasks[name] = task
        task.add_done_callback(report_error_remove_tracking)
        return task

    async def _heartbeat_task(self) -> None:
        """Send a periodic heartbeat"""
        try:
            while self.psmgr.default_pub_socket and not self.psmgr.default_pub_socket.closed:
                await self.psmgr.publish_async(create_heartbeat_message())
                await asyncio.sleep(1)
            LOGGER.warning("Lost self.psmgr.default_pub_socket before heartbeat was cancelled")
        except asyncio.CancelledError:
            LOGGER.debug("Cancelled")
            return

    def _resolve_default_pub_socket(self) -> None:
        """Resolves the path for default PUB socket and sets it to PubSubManager"""
        pub_default = "ipc://" + str(Path(tempfile.gettempdir()) / self.configpath.name.replace(".toml", "_pub.sock"))
        if "zmq" in self.config and "pub_sockets" in self.config["zmq"]:
            pub_default = self.config["zmq"]["pub_sockets"]
        sdesc = ZMQSocketDescription(pub_default, ZMQSocketType.PUB)
        sock = self.psmgr.sockethandler.get_socket(sdesc)
        LOGGER.debug("Setting psmgr@{} default pub socket to {} (sdesc={})".format(hex(id(self.psmgr)), sock, sdesc))
        self.psmgr.default_pub_socket = sock

    async def _stop_hbtask_graceful(self) -> None:
        """Stops the hb task if it's active"""
        if "HEARTBEAT" not in self._tasks:
            return
        await self.stop_named_task_graceful("HEARTBEAT")

    async def _restart_hb_task(self) -> None:
        """Stop and recreate hb task"""
        await self._stop_hbtask_graceful()
        self.create_task(self._heartbeat_task(), name="HEARTBEAT")

    def reload(self) -> None:
        """Load configs, restart sockets"""
        self.psmgr.sockethandler.close_all_sockets()
        with self.configpath.open("rt", encoding="utf-8") as filepntr:
            self.config = toml.load(filepntr)
        self._resolve_default_pub_socket()
        self.create_task(self._restart_hb_task())

    async def stop_named_task_graceful(self, taskname: str) -> Optional[Any]:
        """cancel the named task if it is running and return the result"""
        if taskname not in self._tasks:
            LOGGER.warning("task {} not found".format(taskname), stack_info=True)
            return None
        task = self._tasks[taskname]
        return await self.stop_task_graceful(task)

    async def stop_task_graceful(self, task: "asyncio.Task[Any]") -> Any:
        """cancel the given task if it is running and return the result"""
        if not task.done():
            LOGGER.info("Cancelling task {}".format(task))
            task.cancel()
        try:
            return await task
        except asyncio.CancelledError:
            LOGGER.error("Task {} did not handle cancellation".format(task))

    async def stop_lingering_tasks(self) -> None:
        """Stop all still lingering tasks and fetch their results"""
        # we modify the dictionary during iteration, make a copy of the values
        for task in list(self._tasks.values()):
            try:
                await self.stop_task_graceful(task)
                LOGGER.info("Task {} stopped".format(task))
            except Exception:  # pylint: disable=W0703
                LOGGER.exception("Task {} returned exception".format(task))

    async def teardown(self) -> None:
        """Stop all tasks, close all sockets"""
        await self._stop_hbtask_graceful()
        await self.stop_lingering_tasks()
        self.psmgr.sockethandler.close_all_sockets()


@dataclass
class SimpleService(SimpleServiceMixin, BaseService):
    """Simple service does a bit of automagics in setup"""

    async def setup(self) -> None:
        """Called once by run, just calls reload which loads our config"""
        self.hook_signals()
        self.reload()
