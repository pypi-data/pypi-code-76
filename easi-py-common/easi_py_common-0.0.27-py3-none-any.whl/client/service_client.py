# -*- coding: utf-8 -*-
import inspect
from functools import wraps

from easi_py_common.client.rest_client import RestClient

service_endpoint = {}

HTTP_METHOD_GET = 'GET'
HTTP_METHOD_POST = 'POST'
HTTP_METHOD_PUT = 'PUT'
HTTP_METHOD_DELETE = 'DELETE'


def service_client(url, timeout=(5, 5), http_adapter=None, before_request=None):
    def wrapper(f):
        key = '{}.{}'.format(f.__module__, f.__name__)

        service_endpoint[key] = RestClient(url, timeout=timeout,
                                           http_adapter=http_adapter, before_request=before_request)

        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def service_mapping(uri, method):
    def wrapper(f):
        try:
            is_method = inspect.getargspec(f)[0][0] == 'self'
        except:
            is_method = False

        if not is_method:
            raise Exception('{} is invalid service_mapping', f.__name__)

        @wraps(f)
        def wrapped(*args, **kwargs):
            name = '{}.{}'.format(args[0].__class__.__module__, args[0].__class__.__name__)
            if name not in service_endpoint:
                raise Exception('{}.{} is not have config endpoint', f.__module__, f.__name__)

            _uri = uri.format(**kwargs)
            data = args[1] if len(args) > 1 else None
            if data is None:
                data = kwargs.get('data', None)
            client = service_endpoint[name]
            if method == HTTP_METHOD_GET:
                return client.get(_uri, params=data)
            elif method == HTTP_METHOD_POST:
                return client.post(_uri, json_data=data)
            elif method == HTTP_METHOD_PUT:
                return client.put(_uri, json_data=data)
            elif method == HTTP_METHOD_DELETE:
                return client.delete(_uri, json_data=data)
            else:
                raise Exception('{}.{} is invalid method', f.__module__, f.__name__)

        return wrapped

    return wrapper
