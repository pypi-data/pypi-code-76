# -*- coding: utf-8 -*-
import json
import logging

import requests
from furl import furl


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def _do_verb(verb, url, payload):
    params = {
        'url': url + '.xml',
    }
    method = getattr(requests, verb)

    if verb in ['post', 'put']:
        params['headers'] = {
            'Content-Type': 'application/xml; charset=utf-8'
        }
        params['params'] = 'data=' + payload.decode()
        # params['data'] = payload.decode()
    elif verb == 'get':
        params['params'] = payload

    return method(**params)


class APIClient(object):
    API_VERSION = 'v1'
    API_ENDPOINT = 'https://api.umov.me'
    ARGS = ['subresource', 'subresource_id', 'command']

    def __init__(self, api_key):
        self._api_key = api_key

    def get_options(self, args):
        return [args[k] for k in self.ARGS if k in args and args[k]]

    def make_request(self, resource, **kwargs):
        verb = kwargs.get('verb', 'GET').lower()

        url = furl(self.API_ENDPOINT)
        url.path.segments = [
            'CenterWeb',
            'api',
            self._api_key,
            resource,
        ]

        if kwargs.get('resource_id'):
            url.path.segments.append(kwargs.get('resource_id'))

        url.path.segments.extend(self.get_options(kwargs))

        payload = kwargs.get('extra') or kwargs.get('data')
        verb = _do_verb(verb, str(url), payload=payload)
        return verb
