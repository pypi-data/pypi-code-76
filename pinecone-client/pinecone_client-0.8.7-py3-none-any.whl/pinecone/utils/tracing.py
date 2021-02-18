#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

import logging
import distutils.util
import os


def init_tracer():
    enable_tracing = distutils.util.strtobool(os.getenv('DD_TRACING_ENABLED', default='False'))
    if not enable_tracing:
        os.environ['DD_TRACE_STARTUP_LOGS'] = 'False'

    from ddtrace import tracer, patch_all
    from ddtrace.contrib import asyncio
    tracer.enabled = enable_tracing

    if enable_tracing:
        tracer.context_provider = asyncio.context_provider
        patch_all()


def init_profiler():
    enable_profiling = distutils.util.strtobool(os.getenv('DD_PROFILING_ENABLED', default='False'))
    if enable_profiling:
        import ddtrace.profiling.auto


def get_msg_size(msg: 'core_pb2.Request'):
    request_type = msg.WhichOneof('body')
    if request_type == 'info':
        return 1
    if request_type == "query":
        return msg.query.data.shape[0]
    if request_type == "index":
        return len(msg.index.ids)
    if request_type == "delete":
        return len(msg.delete.ids)
    if request_type == "fetch":
        return len(msg.fetch.ids)


def set_span_tags(span: 'Span', msg: 'core_pb2.Request'):
    span.set_tags({'path': msg.path,
                   'request_type': msg.WhichOneof('body'),
                   'service_name': msg.service_name})
    span.set_metric('msg_size', get_msg_size(msg))  # indicates the batch size


def set_span_service(span: 'Span', service_name: str):
    span.set_tags({'service_name': service_name})

