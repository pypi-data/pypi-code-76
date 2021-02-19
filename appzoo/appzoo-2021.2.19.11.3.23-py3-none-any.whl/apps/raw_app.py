#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : raw_app
# @Time         : 2020/12/28 11:11 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import time

from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *

app = FastAPI()


@app.post('/')
def read_root(kwargs:dict):
    print(kwargs)
    return kwargs

@app.post('/')
def read_root(kwargs:dict):
    print(kwargs)
    return kwargs

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
