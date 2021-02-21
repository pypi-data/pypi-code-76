from . import Socket, SocketType
from .servlet import ZMQServlet
from pinecone.utils.constants import ZMQ_CONTROL_PORT
from pinecone.utils import get_hostname
from pinecone.protos import core_pb2

import zmq

from typing import AsyncIterable


class GatewayServlet(ZMQServlet):

    async def poll_traceroute(self) -> AsyncIterable['core_pb2.TraceRoute']:
        control_sock = self.init_socket(Socket(True, SocketType.PULL, ZMQ_CONTROL_PORT, get_hostname()))
        while True:
            yield await self.recv_traceroute(control_sock)

    async def recv_traceroute(self, sock: zmq.Socket) -> 'core_pb2.TraceRoute':
        msg = await sock.recv()
        msg_pb = core_pb2.TraceRoute()
        msg_pb.ParseFromString(msg)
        self.msg_recv += 1
        return msg_pb
