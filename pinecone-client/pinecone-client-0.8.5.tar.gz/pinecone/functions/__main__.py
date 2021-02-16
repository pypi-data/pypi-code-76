#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from pinecone.utils.tracing import init_tracer, init_profiler
init_tracer()
init_profiler()

import argparse
from pinecone.network.zmq_service import ZMQService

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Load functions with config')

    ZMQService.add_args(parser)

    args = parser.parse_args()
    ZMQService.start_with_args(args)
