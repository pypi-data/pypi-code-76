# -*- coding: utf-8 -*-
import inspect
from functools import wraps
from string import Formatter
from pydantic.main import BaseModel
from easi_py_common.client.rest_client import RestClient, DST_MODE_SERVICE

service_endpoint = {}

HTTP_METHOD_GET = 'GET'
HTTP_METHOD_POST = 'POST'
HTTP_METHOD_PUT = 'PUT'
HTTP_METHOD_DELETE = 'DELETE'


def service_client(url, timeout=(5, 5), http_adapter=None, before_request=None,
                   dst_mode=DST_MODE_SERVICE):
    def wrapper(f):
        key = '{}.{}'.format(f.__module__, f.__name__)

        service_endpoint[key] = RestClient(
            url, timeout=timeout, http_adapter=http_adapter, before_request=before_request,
            dst_mode=dst_mode)

        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapped

    return wrapper


def service_mapping(uri, method, timeout=None, data_by_alias: bool = True, data_key='data'):
    def wrapper(f):
        full_arg_spec = inspect.getfullargspec(f)
        is_method = full_arg_spec.args and full_arg_spec.args[0] == 'self'
        if not is_method:
            raise Exception('{} is invalid service_mapping', f.__name__)

        dst = full_arg_spec.annotations.get('return')
        has_format_names = [fn for _, fn, _, _ in Formatter().parse(uri) if fn is not None]

        def __get_request_params(named_args):
            request_named_args = {k: v for k, v in named_args.items() if k not in has_format_names}
            data = None
            if method == HTTP_METHOD_POST or method == HTTP_METHOD_PUT:
                if data_key in request_named_args:
                    data = request_named_args.pop(data_key)
                if data is None:
                    data = {}

            return request_named_args, data

        def __get_function_args(args, kwargs):
            named_args = inspect.getcallargs(f, *args, **kwargs)
            named_args.update(named_args.pop(full_arg_spec.varkw, {}))
            if ((method == HTTP_METHOD_GET or method == HTTP_METHOD_DELETE)
                    and data_key in named_args and isinstance(named_args[data_key], BaseModel)):
                params_data = named_args.pop(data_key)
                named_args.update(params_data.dict(by_alias=data_by_alias))
            return named_args

        @wraps(f)
        def wrapped(*args, **kwargs):
            name = '{}.{}'.format(args[0].__class__.__module__, args[0].__class__.__name__)
            if name not in service_endpoint:
                raise Exception('{}.{} is not have config endpoint', f.__module__, f.__name__)

            named_args = __get_function_args(args, kwargs)
            _uri = uri.format(**named_args)
            params, data = __get_request_params(named_args)

            client = service_endpoint[name]
            if method == HTTP_METHOD_GET:
                return client.get(_uri, params=params, timeout=timeout, dst=dst)
            elif method == HTTP_METHOD_POST:
                return client.post(_uri, json_data=data, params=params, timeout=timeout, dst=dst,
                                   request_by_alias=data_by_alias)
            elif method == HTTP_METHOD_PUT:
                return client.put(_uri, json_data=data, params=params, timeout=timeout, dst=dst,
                                  request_by_alias=data_by_alias)
            elif method == HTTP_METHOD_DELETE:
                return client.delete(_uri, params=params, timeout=timeout, dst=dst)
            else:
                raise Exception('{}.{} is invalid method', f.__module__, f.__name__)

        return wrapped

    return wrapper


def service_mapping_get(uri, timeout=None, data_by_alias: bool = True, data_key='data'):
    return service_mapping(uri, method=HTTP_METHOD_GET, timeout=timeout,
                           data_by_alias=data_by_alias, data_key=data_key)


def service_mapping_post(uri, timeout=None, data_by_alias: bool = True, data_key='data'):
    return service_mapping(uri, method=HTTP_METHOD_POST, timeout=timeout,
                           data_by_alias=data_by_alias, data_key=data_key)


def service_mapping_put(uri, timeout=None, request_by_alias: bool = True, data_key='data'):
    return service_mapping(uri, method=HTTP_METHOD_PUT, timeout=timeout,
                           data_by_alias=request_by_alias, data_key=data_key)


def service_mapping_delete(uri, timeout=None, request_by_alias: bool = True, data_key='data'):
    return service_mapping(uri, method=HTTP_METHOD_DELETE, timeout=timeout,
                           data_by_alias=request_by_alias, data_key=data_key)
