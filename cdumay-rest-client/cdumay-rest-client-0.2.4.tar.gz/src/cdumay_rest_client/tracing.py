#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import opentracing
import requests
from cdumay_http_client.tracing import RequestSpan
from cdumay_rest_client.client import RESTClient


class OpentracingRestClient(RESTClient):
    def _request_wrapper(self, **kwargs):
        with opentracing.tracer.start_span(
                obj=kwargs, span_factory=RequestSpan) as span:
            RequestSpan.inject(span, kwargs)
            span.obj = requests.request(**kwargs)
            return span.obj
