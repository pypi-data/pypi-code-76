#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.network.zmq import Socket, SocketType
from pinecone.network.zmq.spec import ServletSpec
from pinecone.network.zmq.servlet import ZMQServlet
from pinecone.utils import constants
from pinecone.protos import core_pb2

import docker
from loguru import logger

import asyncio
import time
import abc


class HubModel(abc.ABC):

    def __init__(self, image: str, docker_host: str = 'localhost', config: dict = None, **kwargs):
        self._image = image
        self.docker_client = None
        self.container = None
        self.servlet = None
        self.docker_host = docker_host
        self.executor = None
        self.log_task = None
        self.dns_tasks = []
        self.config = config or {}
        super().__init__(**kwargs)
        self.config['image'] = image

    @property
    def image(self):
        return self._image

    async def call_remote(self, msg: 'core_pb2.Request', timeout: float = 30) -> 'core_pb2.Request':
        if self.servlet is None:
            logger.error('Must start model using `with` syntax before calling remote function')
            raise Exception
        loop = asyncio.get_event_loop()

        loop.create_task(self.servlet.send_msg(msg))

        logger.warning('awaiting message')
        try:
            response = await asyncio.wait_for(self.servlet.recv_msg(self.servlet.zmq_ins[0]), timeout=timeout)
            return response
        except asyncio.TimeoutError:
            logger.error("CONTAINER TIMED OUT. LOGS:")
            logger.error(self.container.logs())
            raise RuntimeError("Model timed out. See more details above. Consider increasing the timeout argument.")

    async def get_container_logs(self):
        while True:
            await asyncio.sleep(0.5)
            if self.container.status not in ['running', 'created']:
                logger.warning(self.container.logs().decode())
                logger.warning('Model container exited, status {status}', status=self.container.status)
                break

    def image_uri(self):
        return self.image

    def start(self):
        if self.container and self.container.status == 'running':
            logger.warning('The container is already running.')

        in_sockets = [Socket(False, SocketType.PULL, port=constants.ZMQ_SECONDARY_PORT, host=self.docker_host)]
        out_sockets = [Socket(False, SocketType.PUSH, port=constants.ZMQ_PORT_IN, host=self.docker_host)]
        servlet_spec = ServletSpec(handle_msg=None, in_sockets=in_sockets, out_sockets={'*': out_sockets}, native=False)

        self.servlet = ZMQServlet(servlet_spec)

        ports = {constants.ZMQ_PORT_IN: constants.ZMQ_PORT_IN, constants.ZMQ_SECONDARY_PORT: constants.ZMQ_SECONDARY_PORT}
        command = ['python3', '-m', 'pinecone.functions.model', *self.to_args()]
        self.docker_client = docker.from_env()
        self.container = self.docker_client.containers.run(self.image_uri(), command, ports=ports, detach=True,
                                                           environment=['PYTHONUNBUFFERED==1',
                                                                        'DD_TRACING_ENABLED=False'])
        time.sleep(1)
        loop = asyncio.get_event_loop()
        self.log_task = loop.create_task(self.get_container_logs())
        self.dns_tasks = self.servlet.refresh_dns()


    def stop(self):
        if self.container:
            self.container.stop()
            self.container = None
        if self.log_task:
            self.log_task.cancel()
        for task in self.dns_tasks:
            task.cancel()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
