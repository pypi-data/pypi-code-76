from asyncio import Queue

from aiozmq import ZmqStream

from interstate_py.control.worker_task import AIOWorkerTask
from interstate_py.log_factory import LogFactory
from interstate_py.zeromq.zmsg_assembly import ZMsgAssembly


class OutboundWorker(AIOWorkerTask):
    """
    The outbound worker accepts messages from a given outbound queue and sends them back to the given client.
    If a message could not be send due to whatever reason a control message is put onto the corresponding queue.

    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self, router: ZmqStream, raw_outbound_queue: Queue, control_queue: Queue):
        super().__init__()
        self._router = router
        self._outbound_queue = raw_outbound_queue
        self._control_queue = control_queue

    async def do_work(self):
        try:
            message_to_send = await self._outbound_queue.get()
            self._router.write(ZMsgAssembly.assemble(message_to_send))
            self._outbound_queue.task_done()
        except Exception as e:
            self._log.error(e)
