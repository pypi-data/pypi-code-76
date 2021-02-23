#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : iapp
# @Time         : 2020/10/22 11:01 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import time
import uvicorn

from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *

from collections import OrderedDict
from traceback import format_exc  # https://www.cnblogs.com/klchang/p/4635040.html


class App(object):
    """
    TODO: 把函数response封装好，支持多个app-run
    """

    def __init__(self, verbose=True):
        self.app = FastAPI()
        self.verbose = verbose

    def run(self, app=None, host="0.0.0.0", port=8000, workers=1, access_log=True, debug=False, reload=False, **kwargs):
        """

        :param app:   app字符串可开启热更新
        :param host:
        :param port:
        :param workers:
        :param access_log:
        :param debug:
        :param reload:
        :param kwargs:
        :return:
        """
        uvicorn.run(
            app if app else self.app,
            host=host, port=port, workers=workers, access_log=access_log, debug=debug, reload=reload, **kwargs
        )

    def add_route(self, path='/xxx', func=lambda x='demo': x, method="GET", **kwargs):

        handler = self._handler(func, method, **kwargs)
        self.app.api_route(path=path, methods=[method])(handler)

    def _handler(self, func, method='GET', result_key='result', **kwargs):
        """

        :param func:
        :param method:
            get -> request: Request
            post -> kwargs: dict
        :param result_key:
        :return:
        """
        if method == 'GET':
            async def handler(request: Request):
                input = dict(request.query_params)
                return self._try_func(input, func, result_key, **kwargs)

        elif method == 'POST':
            async def handler(kwargs_: dict):  # todo 表单 request.form()
                input = kwargs_
                return self._try_func(input, func, result_key, **kwargs)

        else:
            async def handler():
                return {'Warning': 'method not in {"GET", "POST"}'}

        return handler

    def _try_func(self, kwargs, func, result_key='result', **kwargs_):
        input = kwargs
        output = OrderedDict()

        if self.verbose:
            output['RequestParams'] = input

        try:
            output['suceess'] = 1
            output[result_key] = func(**input)

        except Exception as error:
            output['suceess'] = 0
            output['Error'] = error
            output['ErrorPlus'] = format_exc().strip()

        finally:
            output.update(kwargs_)

        return output

    def app_file_name(self, file):
        """
        file = __file__
        """
        print(file)
        _ = file.split('/')[-1].split('.')[0]
        return f"{_}:app"


if __name__ == '__main__':
    import uvicorn

    app = App()
    app.add_route('/get', lambda **kwargs: kwargs, method="GET", result_key="GetResult")
    app.add_route('/post', lambda **kwargs: kwargs, method="POST", result_key="PostResult")

    app.run(port=9000, debug=False, reload=False)
    # app.run(f"{app.app_file_name(__file__)}", port=9000, debug=False, reload=False)
