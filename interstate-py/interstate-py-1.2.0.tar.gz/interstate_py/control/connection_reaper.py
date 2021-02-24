import asyncio

from interstate_py.connection_agent import ConnectionAgentBase
from interstate_py.control.worker_task import AIOWorkerTask
from interstate_py.log_factory import LogFactory


class ConnectionReaper(AIOWorkerTask):
    """
    Reaps connections that are closed on both ends (client and server side stream) within a given interval.
    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self, con_agent: ConnectionAgentBase, reap_interval: float = 5.0):
        super().__init__()
        self._con_agent = con_agent
        self._interval = reap_interval

    async def do_work(self):
        await asyncio.sleep(self._interval)
        closed_connections = filter(lambda con: con.closed_count() == 2, self._con_agent.connections())
        self._con_agent.dump_all(map(lambda closed_con: closed_con.identity(), closed_connections))
