#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.utils.tracing import init_tracer, init_profiler
init_tracer()
init_profiler()

from pinecone.network.zmq import Socket, SocketType, entrypoints
from pinecone.network.zmq.spec import ServletSpec
from pinecone.utils import load_hub_service, constants
from pinecone import functions

import argparse
import importlib
import json
import asyncio

import concurrent.futures
from functools import partial

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Load functions with config')
    functions.Function.add_args(parser)

    args, unk = parser.parse_known_args()

    model = importlib.import_module('model')

    custom_model_cls = load_hub_service(model)
    transformer_service = custom_model_cls(**json.loads(args.config))

    executor = concurrent.futures.ThreadPoolExecutor()

    async def call_handler(msg):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, partial(transformer_service.handle_msg, msg))

    in_sockets = [Socket(True, SocketType.PULL, port=constants.ZMQ_PORT_IN)]
    out_sockets = [Socket(True, SocketType.PUSH, port=constants.ZMQ_SECONDARY_PORT)]
    spec = ServletSpec(handle_msg=call_handler, in_sockets=in_sockets, out_sockets={'*': out_sockets}, native=False,
                       service_name=transformer_service.name)
    entrypoints.start(spec)
