#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>

"""
import json
import logging

from cdumay_http_client.client import HttpClient

logger = logging.getLogger(__name__)


class RESTClient(HttpClient):
    """RestClient"""

    def __init__(self, server, timeout=None, headers=None, username=None,
                 password=None, ssl_verify=True, retry_number=None,
                 retry_delay=None):
        _headers = headers or dict()
        _headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        HttpClient.__init__(
            self, server, timeout, _headers, username, password, ssl_verify,
            retry_number, retry_delay
        )

    def _format_data(self, data):
        return json.dumps(data) if data else None

    # noinspection PyMethodMayBeStatic
    def _parse_response(self, response):
        return response.json()
