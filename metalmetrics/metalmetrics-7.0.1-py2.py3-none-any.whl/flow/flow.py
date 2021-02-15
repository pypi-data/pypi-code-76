# -*- coding: utf-8 -*-

import grpc

from concurrent import futures
from metalmetrics.flow.flow_pb2 import FlowReply
from metalmetrics.flow.flow_pb2_grpc import (
    add_FlowProtoServicer_to_server,
    FlowProtoServicer,
)

MSG_PREFIX = "metalmetrics/metrics"
MSG_SEP = "/"


class FlowException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Flow(object):
    _workers = 10

    def __init__(self, config):
        if config is None:
            raise FlowException("config invalid")
        self._config = config

    def _serve(self, routine):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._workers))
        add_FlowProtoServicer_to_server(FlowProto(routine), server)
        server.add_insecure_port(self._config.listen_url)
        server.start()
        server.wait_for_termination()

    def run(self, routine):
        self._serve(routine)


class FlowProto(FlowProtoServicer):
    def __init__(self, routine):
        self._routine = routine

    def SendFlow(self, request, _):
        if len(request.message) == 0 or not request.message.startswith(
            MSG_PREFIX + MSG_SEP
        ):
            return FlowReply(message="")
        msg = MSG_SEP.split(request.message)
        if len(msg) == len(MSG_SEP.split(MSG_PREFIX)):
            buf = self._routine()
        elif len(msg) == len(MSG_SEP.split(MSG_PREFIX) + 1):
            buf = self._routine(msg[-1])
        else:
            buf = ""
        return FlowReply(message=buf)
