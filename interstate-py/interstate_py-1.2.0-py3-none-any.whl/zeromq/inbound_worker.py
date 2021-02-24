from asyncio import Queue

from aiozmq import ZmqStream

from interstate_py.control.worker_task import AIOWorkerTask
from interstate_py.log_factory import LogFactory
from interstate_py.zeromq.zmsg_assembly import ZMsgAssembly


class InboundWorker(AIOWorkerTask):
    """
    Accepts inbound message from the zmq router (aka ZmqStream) and dispatches them to the inbound queue
    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self, router: ZmqStream, inbound_queue: Queue):
        super().__init__()
        self._router = router
        self._inbound_queue = inbound_queue

    async def do_work(self):
        try:
            zmsg = await self._router.read()
            wire_message = ZMsgAssembly.disassemble(zmsg)
            await self._inbound_queue.put(wire_message)
        except Exception as e:
            self._log.error(e)
