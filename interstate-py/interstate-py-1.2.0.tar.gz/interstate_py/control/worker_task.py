import asyncio
from abc import ABC, abstractmethod

from interstate_py.log_factory import LogFactory


class AIOWorkerTask(ABC):
    """
    A asyncio worker task provides a coroutine that can be used as worker around asycio queues to fulfil
    specific long-running tasks.
    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self):
        self._running = False

    @abstractmethod
    async def do_work(self):
        raise NotImplementedError()

    async def start(self):
        self._log.info("started")
        self._running = True
        while self._running:
            try:
                await self.do_work()
            except asyncio.CancelledError:
                self._log.info("Cancel received")
                self._running = False
        self._log.info("{} cancelled".format(__name__))
