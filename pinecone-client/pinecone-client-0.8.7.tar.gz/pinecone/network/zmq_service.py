#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.functions import Function
from pinecone.runnable import Runnable
from pinecone.network.zmq import Socket, ServletSpec, entrypoints
from pinecone.network.selector.shards import ShardSelector
from pinecone.utils.constants import ZMQ_PORT_IN, ZMQ_LOG_PORT, ZMQ_CONTROL_PORT
from pinecone.utils import load_hub_service, module_name, parse_hostname, get_hostname
from pinecone.protos import core_pb2

import concurrent.futures
import asyncio
import json
from typing import Dict, List, Optional
from pydoc import locate
import os
import random
import importlib
import argparse
import traceback

from loguru import logger
from ddtrace.contrib.asyncio import run_in_executor


class ZMQService(Runnable):

    @classmethod
    def from_args(cls, args):
        """
        :param functions:
        :param args:
        :return:
        """
        # logger.warning("loading {functions}", functions=args.function)
        if args.function in ['pinecone.functions.model.transformer.hub.HubTransformer',
                             'pinecone.functions.model.scorer.hub.HubScorer',
                             'pinecone.functions.model.HubFunction']:

            model = importlib.import_module('model')
            service_cls = load_hub_service(model)
            logger.info('loaded functions class {cls}', cls=service_cls)
            args.config = json.dumps(
                {k: v for k, v in json.loads(args.config).items() if k != 'image'})
        else:
            service_cls = locate(args.function)
        service = service_cls.from_args(args)
        return cls(service, json.loads(args.next), args.service, native=args.native)

    def to_args(self):
        """
        Return the command line args to run this instance
        :return:
        """
        return ['pinecone.functions',
                '--function', module_name(self.function),
                '--next', json.dumps(self.next_services,
                                     separators=(',', ':')),
                '--service', self.service_name,
                *(['--native'] if self.native else []),
                *self.function.to_args()]

    @classmethod
    def add_args(cls, parser: argparse.ArgumentParser):
        parser.add_argument('--function', type=str,
                            help='module of functions class to run')
        parser.add_argument('--next', type=str,
                            help='mapping of next functions in the DAG')
        parser.add_argument('--native', action='store_true')
        parser.add_argument('--service', type=str,
                            help='name of the running runner')
        Function.add_args(parser)

    @classmethod
    def start_with_args(cls, args):
        servlet = cls.from_args(args)
        servlet.start()

    def __init__(self, function: Function, next_services: Dict[str, List[str]], service_name: str, native=True):
        """
        :param service: The functions to mount with a ZMQServlet
        :param next: The next functions in the DAG
        """

        self.function = function
        self.next_services = next_services
        self.native = native
        self.service_name = service_name
        self.executor = None

    def get_sockets(self):
        out_type = self.function.out_sock_type
        in_type = self.function.in_sock_type

        in_sockets = [Socket(True, in_type,
                             host=get_hostname(),
                             port=ZMQ_PORT_IN)]

        out_sockets = {r: [Socket(False, out_type, host=s, port=ZMQ_PORT_IN) for s in n] for r, n in
                       self.next_services.items() if n}

        return in_sockets, out_sockets

    async def proxy_msg(self, msg):
        return msg

    async def run_handler_in_executor(self, msg: 'core_pb2.Request'):
        loop = asyncio.get_event_loop()
        if self.executor is None:
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        try:
            result = await run_in_executor(loop, self.executor, self.function.handle_msg, msg)
            return result
        except Exception as e:
            msg.status.code = core_pb2.Status.StatusCode.ERROR
            details = core_pb2.Status.Details(function=self.name,
                                              function_id=get_hostname(),
                                              exception=str(e),
                                              traceback=traceback.format_exc())
            details.time.GetCurrentTime()
            msg.status.details.append(details)
            logger.error(details.traceback)
            return msg

    def start(self, hostname=None):
        # FORMAT: <function.name>-s<shard_id>-r<replica_id>]
        if hostname:
            os.environ['HOSTNAME'] = hostname
        hostname = get_hostname()

        if hostname is None:
            raise RuntimeError('Must set HOSTNAME to run 0mq service')

        parsed_shard, parsed_replica = parse_hostname(self.name, hostname)

        # XXX[Fei]: chance of collision?
        replica_id = random.randint(1, 999999) if parsed_replica is None else parsed_replica
        shard_id = 0 if parsed_shard is None else parsed_shard
        logger.debug(f"PARSED SHARD: {shard_id}, PARSED REPLICA: {replica_id} hostname: {hostname}")

        self.function.id = replica_id
        in_sockets, out_sockets = self.get_sockets()

        selector = ShardSelector()

        servlet_spec = ServletSpec(self.run_handler_in_executor, in_sockets, out_sockets, selector, self.native,
                                   self.function.name, shard_id, replica_id,
                                   self.function.get_stats,
                                   service_name=self.service_name)

        self.function.setup()

        entrypoints.start(servlet_spec, wal=self.volume_request,
                          persistent_dir=os.path.join(self.function.default_persistent_dir, 'wal'),
                          num_replicas=self.replicas, sync_handler=self.function.handle_msg)

    def cleanup(self):
        self.function.cleanup()

    @property
    def name(self):
        return self.function.name

    @property
    def image(self):
        return self.function.image

    @property
    def replicas(self) -> int:
        return self.function.replicas

    @property
    def shards(self) -> int:
        return self.function.shards

    @property
    def ports(self) -> List[int]:
        return [ZMQ_PORT_IN, ZMQ_LOG_PORT, ZMQ_CONTROL_PORT]

    @property
    def ext_port(self) -> Optional[int]:
        return

    @property
    def memory_request(self) -> int:
        return self.function.memory_request

    @property
    def volume_request(self) -> Optional[int]:
        return self.function.volume_request
