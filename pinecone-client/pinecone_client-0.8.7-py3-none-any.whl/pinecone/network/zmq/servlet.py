from pinecone.protos import core_pb2
from pinecone.utils import constants
from pinecone.utils import get_hostname, replica_kube_hostname, replica_name, tracing
from pinecone.network.zmq.spec import ServletSpec, SocketType, Socket
from pinecone.network.zmq.socket_wrapper import SocketWrapper

from loguru import logger
from typing import List
import asyncio
import zmq
import zmq.asyncio


class ZMQServlet:

    def __init__(self, servlet_spec: ServletSpec):
        self.spec = servlet_spec
        self.context = zmq.asyncio.Context()

        self.exception = None
        if len(self.spec.in_sockets) > 0:
            self.zmq_ins = [self.init_socket(in_sock) for in_sock in self.spec.in_sockets]
        self.zmq_outs = {r: [self.init_socket(s) for s in sockets] for r, sockets in self.spec.out_sockets.items()}

        self.msg_sent = 0
        self.msg_recv = 0
        self.gateway_outs = []
        self.gateway_control = {}

    def gateway_control_sock(self, replica: int) -> SocketWrapper:
        if replica not in self.gateway_control:
            self.gateway_control[replica] = self.init_socket(Socket(False, SocketType.PUSH,
                                                                    constants.ZMQ_CONTROL_PORT,
                                                                    host=self.gateway_host(replica)))
        return self.gateway_control[replica]

    @property
    def pretty_name(self) -> str:
        return self.spec.function_name + " shard:" + str(self.spec.shard) + " replica:" + str(self.spec.replica)

    async def handle_msg(self, msg: core_pb2.Request):
        from ddtrace import tracer
        from ddtrace.tracer import Context

        route = core_pb2.Route(function=get_hostname(), function_id=self.spec.shard)
        route.start_time.GetCurrentTime()

        msg_context = Context(trace_id=msg.telemetry_trace_id, span_id=msg.telemetry_parent_id)
        tracer.context_provider.activate(msg_context)
        with tracer.trace(self.spec.function_name) as span:
            tracing.set_span_tags(span, msg)
            msg.telemetry_parent_id = span.span_id
            if self.spec.handle_msg:
                response = await self.spec.handle_msg(msg)
                route.end_time.GetCurrentTime()
                msg.routes.append(route)
                if response:
                    if self.spec.shard != 0:
                        response.shard_num = self.spec.shard
                    await self.send_msg(response)

    async def poll_sock(self, sock: SocketWrapper):
        while True:
            msg = await self.recv_msg(sock)
            await self.handle_msg(msg)

    def start_polling(self) -> List[asyncio.Task]:
        loop = asyncio.get_event_loop()
        return [loop.create_task(self.poll_sock(sock)) for sock in self.zmq_ins]

    def refresh_dns(self) -> List[asyncio.Task]:
        loop = asyncio.get_event_loop()
        return [loop.create_task(sock.refresh_dns()) for sock in self.all_socks]

    def gateway_host(self, replica: int):
        return replica_name(constants.GATEWAY_NAME, 0, replica) if self.spec.native \
            else replica_kube_hostname(constants.GATEWAY_NAME, 0, replica)

    def get_gateway_sock(self, gateway_num: int, sock: Socket) -> SocketWrapper:
        while gateway_num >= len(self.gateway_outs):
            new_sock = Socket(sock.bind, sock_type=sock.sock_type, port=sock.port,
                              host=self.gateway_host(len(self.gateway_outs)))
            self.gateway_outs.append(self.init_socket(new_sock))
        return self.gateway_outs[gateway_num]

    async def send_msg(self, msg: 'core_pb2.Request'):
        self.msg_sent += 1
        send_sockets = []
        for path in {msg.path, '*'}:
            for sock in (sock for sock in self.spec.out_sockets.get(path, []) if sock.host == constants.GATEWAY_NAME):
                send_sockets.append(self.get_gateway_sock(msg.gateway_num, sock))
                break
            else:
                send_sockets.extend(self.zmq_outs.get(path, []))

        if len(send_sockets) == 0:
            logger.warning('{}: no out socket_spec for path {}'.format(get_hostname(), msg.path))

        shard_msgs = self.spec.out_socket_selector.select_socket(msg, len(send_sockets))
        for socket, shard_msg in zip(send_sockets, shard_msgs):
            if shard_msg is not None:
                await socket.send(shard_msg.SerializeToString())

        if msg.traceroute:
            receipt = core_pb2.TraceRoute(request_id=msg.request_id, client_id=msg.client_id,
                                          client_offset=msg.client_offset, routes=msg.routes)
            await self.gateway_control_sock(msg.gateway_num).send(receipt.SerializeToString())

    async def recv_msg(self, sock: SocketWrapper) -> 'core_pb2.Request':
        msg = await sock.recv()
        msg_pb = core_pb2.Request()
        msg_pb.ParseFromString(msg)
        self.msg_recv += 1
        return msg_pb

    def init_socket(self, socket: Socket):
        return SocketWrapper(socket, self.context, self.spec.native)

    @property
    def all_socks(self):
        return [*self.zmq_ins, *[sock for sock_list in self.zmq_outs.values() for sock in sock_list]]

    def cleanup(self):
        for sock in self.all_socks:
            sock.close()
