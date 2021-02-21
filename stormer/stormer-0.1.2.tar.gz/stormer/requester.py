#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created By Murray(m18527) on 2019/12/13 13:57
"""
import json as _json
import logging
import os
from collections import namedtuple
from urllib.parse import urljoin

import chardet
import requests
from urllib3 import encode_multipart_formdata

from .redis_utils import get_redis_cache

logger = logging.getLogger(__name__)

VERSION = "0.1.2"

DEBUG = os.getenv("DEBUG", False)

Resp = namedtuple("Resp", ["status_code", "content", "reason"])

META_CACHE_KEY = "REQUESTER:META:{PARAMS_HASH}"
CONTENT_CACHE_KEY = "REQUESTER:CONTENT:{PARAMS_HASH}"


class RespResult(object):
    """
    Used for packing request response
    """

    def __init__(self, response=None, url=None, action=None, params_hash=None, redis_cache=None, encoding=None):
        if not isinstance(response, requests.Response):
            msg = "Param <response> should be object of requests.Response, but {} found.".format(type(response))
            logger.warning(msg)
            raise Exception(msg)
        self.response = response
        self.ok = None
        self.reason = None
        self.content = None
        self.headers = None
        self.encoding = encoding
        self.status_code = None
        self.url = url
        self.action = action
        self.params_hash = params_hash
        self.redis_cache = redis_cache
        self._init()

    def _init(self):
        if self.encoding:
            self.response.encoding = self.encoding
        self.encoding = self.response.encoding
        self.ok = self.response.ok
        self.reason = self.response.reason
        self.content = self.response.content
        self.text = self.response.text
        self.headers = self.response.headers.__repr__()

        self.status_code = self.response.status_code

    @staticmethod
    def guest_encoding(text):
        """The apparent encoding, provided by the chardet library."""
        return chardet.detect(text)['encoding']

    @property
    def bytes(self):
        return self.content

    @property
    def json(self):
        return self.response.json()

    @property
    def data(self):
        try:
            _data = self.json
        except (Exception,):
            _data = self.text
            if not _data:
                _data = self.bytes
        return _data

    @property
    def resp(self):
        """
        parse resp to api resp
        """
        if 200 <= self.status_code < 300:
            return Resp(status_code=self.status_code, content=self.data, reason=None)
        if isinstance(self.reason, bytes):
            try:
                reason = self.reason.decode(self.encoding or "utf-8")
            except UnicodeDecodeError:
                reason = self.reason.decode('iso-8859-1')
        else:
            reason = self.reason
        logger.error("The request failed, http status code: {status}, content: {content}, reason: {reason}".format(
            status=self.status_code, content=self.data, reason=self.reason))
        return Resp(status_code=self.status_code, content=self.data, reason=reason)

    def set_cache(self, timeout):
        if not (timeout > 0 and self.redis_cache and self.params_hash) \
                or not str(self.action).upper() == "GET":
            return None
        meta_data = {
            "ok": self.ok,
            "reason": self.reason,
            "text": self.text,
            "headers": self.headers,
            "encoding": self.encoding,
            "status_code": self.status_code,
            "url": self.url,
            "action": self.action,
        }
        meta_key = META_CACHE_KEY.format(PARAMS_HASH=self.params_hash)
        content_key = CONTENT_CACHE_KEY.format(PARAMS_HASH=self.params_hash)
        self.redis_cache.set(meta_key, _json.dumps(meta_data), ex=timeout)
        self.redis_cache.set(content_key, self.content, ex=timeout)

    @classmethod
    def from_cache(cls, params_hash, action, redis_conn):
        if not (redis_conn and action and action.upper() == "GET"):
            return None
        meta_key = META_CACHE_KEY.format(PARAMS_HASH=params_hash)
        content_key = CONTENT_CACHE_KEY.format(PARAMS_HASH=params_hash)
        meta_data = redis_conn.get(meta_key)
        content = redis_conn.get(content_key)
        if not (meta_data and content):
            return None
        result = cls()
        for key, value in _json.loads(meta_data).items():
            setattr(result, key, value)
        setattr(result, "content", content)
        logger.debug("Fetch data from the cache by hash {}.".format(params_hash))
        return result


class Requester(object):
    """Requester is request Class which base on questions, it be used for send request."""
    debug = False

    @staticmethod
    def set_debugging():
        if not Requester.debug:
            global logger
            logger = logging.getLogger("requester")
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                "%(asctime)s - [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
            Requester.debug = True

    def __init__(self, server_url, headers=None, proxies=None, encoding=None,
                 redis_url=None, redis_nodes=None, redis_password='', timeout=0):
        """
        Init Requester
        :param server_url string 'https://xxx.com'
        :param headers dict {'Content-Type': 'application/json'}
        :param proxies dict {"http": None, "https": None}
        :param redis_url string 'redis://:<password>@<host>:<port>/<db>'
        :param redis_nodes string 'ip:port,ip:port'
        :param redis_password string  'redis password'
        """
        self.headers = headers
        self.proxies = proxies or {"http": None, "https": None}
        self.server_url = server_url
        self.redis_url = redis_url
        self.redis_nodes = redis_nodes
        self.redis_password = redis_password
        self.timeout = timeout
        self.encoding = encoding
        self.cache = None
        self.apis = []

        if self.redis_url or self.redis_nodes:
            self.cache = get_redis_cache(redis_url=redis_url, redis_nodes=redis_nodes, password=self.redis_password)

    @staticmethod
    def gen_md5(text, salt='_stormer_requester_'):
        import hashlib
        md = hashlib.md5()
        md.update("{}{}".format(text, salt).encode("utf-8"))
        res = md.hexdigest()
        return res

    @classmethod
    def build_params_hash(cls, url, params, **kwargs):
        new_params = {k: v for k, v in (params or {}).items()}
        new_params.update({"url": url})
        new_params.update(kwargs)
        new_params = _json.dumps(new_params, sort_keys=True)
        return str(cls.gen_md5(new_params)).upper()

    @staticmethod
    def _path_url(url, path_params):
        if path_params and isinstance(path_params, dict):
            url = url.format(**path_params)
        return url

    def _bind_func(self, pre_url, action, timeout=0):
        def req(path_params=None, params=None, data=None, json=None, files=None, forms=None, **kwargs):
            url = self._path_url(pre_url, path_params)
            params_hash, resp_result = None, None
            if self.cache and timeout > 0:
                params_hash = self.build_params_hash(url, params, **kwargs)
                resp_result = RespResult.from_cache(params_hash, action, self.cache)
            if not resp_result:
                resp = self._do_request(
                    action=action, url=url, params=params, data=data, json=json,
                    files=files, forms=forms, **kwargs
                )
                resp_result = RespResult(
                    response=resp, url=url, action=action,
                    redis_cache=self.cache, params_hash=params_hash,
                    encoding=self.encoding
                )
                resp_result.set_cache(timeout)
            return resp_result

        return req

    def _add_path(self, action, uri, func_name, timeout=0):
        action = action.upper()
        func_name = func_name.lower()
        assert func_name not in self.apis, u"Duplicate function {}.".format(func_name)
        url = urljoin(self.server_url, uri)
        setattr(self, func_name, self._bind_func(url, action, timeout=timeout))
        self.apis.append(func_name)
        logger.debug("Requester register method: {method}, path: {url}".format(method=func_name, url=url))
        return getattr(self, func_name)

    @staticmethod
    def _func_name(func):
        try:
            func_name = func.__name__
        except (Exception,):
            func_name = str(func)
        return func_name

    def register(self, action, func, uri, timeout=0):
        func_name = self._func_name(func)
        return self._add_path(action, uri, func_name, timeout=timeout or self.timeout)

    def _headers(self, headers):
        """combine headers"""
        if headers and isinstance(headers, dict):
            if self.headers:
                for key, value in self.headers.items():
                    if key in headers:
                        continue
                    headers[key] = value
        else:
            headers = self.headers
        return headers

    def _proxies(self, proxies):
        """combine proxies"""
        if proxies and isinstance(proxies, dict):
            if self.proxies:
                for key, value in self.headers.items():
                    if key in proxies:
                        continue
                    proxies[key] = value
        else:
            proxies = self.proxies
        return proxies

    def _do_request(self, action, url, params=None, data=None, json=None, files=None, forms=None, **kwargs):
        assert url, "request url can't be blank."
        kwargs["headers"] = self._headers(kwargs.get("headers"))
        kwargs["proxies"] = self._proxies(kwargs.get("proxies"))
        if isinstance(forms, dict):
            if isinstance(data, dict):
                forms.update(data)
            encode_data = encode_multipart_formdata(forms)
            data = encode_data[0]
            if isinstance(kwargs["headers"], dict):
                kwargs["headers"]["Content-Type"] = encode_data[1]
            else:
                kwargs["headers"] = {"Content-Type": encode_data[1]}

        if action.upper() == "GET":
            return requests.get(url, params=params, **kwargs)
        elif action.upper() == "POST":
            return requests.post(url, data=data, json=json, files=files, **kwargs)
        elif action.upper() == "PUT":
            return requests.put(url, data=data, json=json, files=files, **kwargs)
        elif action.upper() == "DELETE":
            return requests.delete(url, **kwargs)
        elif action.upper() == "OPTIONS":
            return requests.options(url, **kwargs)
        else:
            msg = "Not Support %s." % action.upper()
            logger.error(msg)
            raise Exception(msg)


if DEBUG:
    Requester.set_debugging()
