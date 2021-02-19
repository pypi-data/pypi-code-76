# -*- coding: utf-8 -*-
import json

import requests
from flask import current_app
from pydantic.main import ModelMetaclass, BaseModel
from requests.adapters import HTTPAdapter

from easi_py_common.core.error import ServiceException

HEADER = {'Content-Type': 'application/json; charset=UTF-8'}
DST_MODE_SERVICE = 'service'
DST_MODE_OTHER = 'other'


class RestClient:
    def __init__(self, url, timeout=(5, 5), http_adapter=None, before_request=None,
                 dst_mode=DST_MODE_SERVICE):
        self.url = url
        if http_adapter is None:
            http_adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=3)
        session = requests.Session()
        session.mount('http://', http_adapter)
        session.mount('https://', http_adapter)

        self.session = session
        self.timeout = timeout
        self.before_request = before_request
        self.dst_mode = dst_mode

    def _get_url(self, uri):
        if 'SERVICE_CLIENT' in current_app.config and 'http' not in self.url:
            service_client_keys = current_app.config['SERVICE_CLIENT']
            self.url = self.url.format(**service_client_keys)
        return self.url + uri

    def get(self, uri, params=None, timeout=None, dst=None, **kwargs):
        if timeout is None:
            timeout = self.timeout

        _url = self._get_url(uri)

        if callable(self.before_request):
            _request_parms = {
                'url': _url,
                'method': 'GET',
                'params': params,
            }
            _kwargs = self.before_request(_request_parms)
            kwargs.update(_kwargs)

        resp = self.session.get(
            _url,
            params=params,
            timeout=timeout,
            **kwargs
        )
        return self._do_response(resp, dst=dst)

    def post(self, uri, json_data=None, params=None, timeout=None, dst=None, **kwargs):
        if timeout is None:
            timeout = self.timeout

        _url = self._get_url(uri)
        data = None
        if json_data:
            data = (json.dumps(json_data.dict())
                    if isinstance(json_data, BaseModel)
                    else json.dumps(json_data))

        if callable(self.before_request):
            _request_parms = {
                'url': _url,
                'method': 'POST',
                'data': data,
            }
            _kwargs = self.before_request(_request_parms)
            kwargs.update(_kwargs)

        if 'headers' in kwargs:
            kwargs.get('headers').update(HEADER)
        else:
            kwargs['headers'] = HEADER

        resp = self.session.post(
            _url,
            data=data,
            params=params,
            timeout=timeout,
            **kwargs
        )
        return self._do_response(resp, dst=dst)

    def put(self, uri, json_data=None, params=None, timeout=None, dst=None, **kwargs):
        if timeout is None:
            timeout = self.timeout

        _url = self._get_url(uri)

        data = None
        if json_data:
            data = (json.dumps(json_data.dict())
                    if isinstance(json_data, BaseModel)
                    else json.dumps(json_data))

        if callable(self.before_request):
            _request_parms = {
                'url': _url,
                'method': 'PUT',
                'data': data,
            }
            _kwargs = self.before_request(_request_parms)
            kwargs.update(_kwargs)

        if 'headers' in kwargs:
            kwargs.get('headers').update(HEADER)
        else:
            kwargs['headers'] = HEADER

        resp = self.session.put(
            _url,
            data=data,
            params=params,
            timeout=timeout,
            **kwargs
        )
        return self._do_response(resp, dst=dst)

    def delete(self, uri, params=None, timeout=None, dst=None, **kwargs):
        if timeout is None:
            timeout = self.timeout

        _url = self._get_url(uri)
        if callable(self.before_request):
            _request_parms = {
                'url': _url,
                'method': 'DELETE',
            }
            _kwargs = self.before_request(_request_parms)
            kwargs.update(_kwargs)

        resp = self.session.delete(
            _url,
            params=params,
            timeout=timeout,
            **kwargs
        )
        return self._do_response(resp, dst=dst)

    def _do_response(self, response, dst=None):
        status_code = response.status_code
        if status_code == 200:
            result = response.json()
            if (
                    isinstance(result, bool)
                    or isinstance(result, int)
                    or isinstance(result, float)
                    or isinstance(result, str)
            ):
                return result

            if self.dst_mode == DST_MODE_SERVICE:
                code = result.get('code', 0)
                if code != 0:
                    raise ServiceException(code=code, msg=result.get('message', ''))
                result = result.get('data')

            if dst and dst.__class__ == ModelMetaclass:
                return dst.parse_obj(result)
            return result

        if 400 <= status_code < 500:
            raise ServiceException(code=status_code, msg=response.content)
        else:
            raise ServiceException(code=status_code, msg=response.content)
