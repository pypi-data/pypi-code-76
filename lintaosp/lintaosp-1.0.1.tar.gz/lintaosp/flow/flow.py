# -*- coding: utf-8 -*-

import base64
import grpc
import json
import os
import pathlib
import shutil
import tempfile

from concurrent import futures
from lintaosp.flow.flow_pb2 import FlowReply
from lintaosp.flow.flow_pb2_grpc import (
    add_FlowProtoServicer_to_server,
    FlowProtoServicer,
)

MAX_WORKERS = 10

MSG_PREFIX = "lintaosp/aosp"
MSG_SEP = "/"


class FlowException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Flow(object):
    def __init__(self, config):
        if config is None:
            raise FlowException("config invalid")
        self._config = config

    def _serve(self, routine):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
        add_FlowProtoServicer_to_server(FlowProto(routine), server)
        server.add_insecure_port(self._config.listen_url)
        server.start()
        server.wait_for_termination()

    def run(self, routine):
        self._serve(routine)


class FlowProto(FlowProtoServicer):
    def __init__(self, routine):
        self._routine = routine

    def _build(self, data):
        def _helper(root, dirs, file, data):
            pathlib.Path(os.path.join(root, dirs)).mkdir(parents=True, exist_ok=True)
            p = pathlib.Path(os.path.join(root, dirs, file))
            with p.open("w") as f:
                f.write(base64.b64decode(data).decode("utf-8"))

        if len(data) == 0:
            return None
        buf = json.loads(data)
        root = tempfile.mkdtemp(prefix=MSG_PREFIX.replace("/", "-") + "-")
        for key, val in buf.items():
            _helper(root, os.path.dirname(key), os.path.basename(key), val)

        return root

    def _clean(self, project):
        if os.path.exists(project):
            shutil.rmtree(project)

    def SendFlow(self, request, _):
        if len(request.message) == 0 or not request.message.startswith(MSG_PREFIX):
            return FlowReply(message="")
        msg = MSG_SEP.split(request.message)
        if len(msg) == len(MSG_SEP.split(MSG_PREFIX)):
            return FlowReply(message="")
        elif len(msg) > len(MSG_SEP.split(MSG_PREFIX)):
            project = self._build(
                request.message.replace(MSG_PREFIX + MSG_SEP, "").strip()
            )
            if project is None or not os.path.exists(project):
                return FlowReply(message="")
            buf = self._routine(project)
            self._clean(project)
        else:
            buf = ""
        return FlowReply(message=buf)
