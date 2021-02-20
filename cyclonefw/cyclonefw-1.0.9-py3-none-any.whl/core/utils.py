#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from flask import abort
import cyclonefw
from cyclonefw.utils.image_utils import ImageProcessor
import os, logging
from logging.handlers import RotatingFileHandler
import json
import requests


def redirect_errors_to_flask(func):
    """
    This decorator function will capture all Pythonic errors and return them as flask errors.

    If you are looking to disable this functionality, please remove this decorator from the `apply_transforms()` module
    under the ImageProcessor class.
    """

    def inner(*args, **kwargs):
        try:
            # run the function
            return func(*args, **kwargs)
        except ValueError as ve:
            if 'pic should be 2 or 3 dimensional' in str(ve):
                abort(400, "Invalid input, please ensure the input is either "
                           "a grayscale or a colour image.")
        except TypeError as te:
            if 'bytes or ndarray' in str(te):
                abort(400, "Invalid input format, please make sure the input file format "
                           " is a common image format such as JPG or PNG.")

    return inner


class MAXImageProcessor(ImageProcessor):
    """Composes several transforms together.

    Args:
        transforms (list of ``Transform`` objects): list of transforms to compose.

    Example:
        >>> pipeline = ImageProcessor([
        >>>     Rotate(150),
        >>>     Resize([100,100])
        >>> ])
        >>> pipeline.apply_transforms(img)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @redirect_errors_to_flask
    def apply_transforms(self, img):
        return super().apply_transforms(img)


class AppFilter(logging.Filter):
    def __init__(self):
        pass

    def filter(self, record):
        record.app_name = cyclonefw.core.app.context.app_name
        try:
            trace_id = cyclonefw.core.app.getTraceId()
        except Exception as e:
            print(e)
        else:
            record.trace_id = trace_id

        return True


def getLogger(name="cyclonefw", formatter="[%(asctime)s] [%(pathname)s(line:%(lineno)d)] [%(levelname)s] %(message)s",
              logPath=None, level=logging.DEBUG):
    """
    获取logger

    日志记录使用如下格式: %s 等作为占位符

    print "My name is %s and weight is %d kg!" % ('Zara', 21)

    :param name: 日志名称
    :param formatter: 日志格式
    :param logPath: 日志目录, 默认为 logs目录下, 使用 . 可以指定当前执行目录
    :param level: 日志级别
    :return:
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        consolelog = logging.StreamHandler()
        consolelog.setFormatter(logging.Formatter(formatter))
        logger.addHandler(consolelog)
        logger.addFilter(AppFilter())

    if logPath != None:
        logger.addHandler(logHandler(name, formatter, logPath))

    return logger


def logHandler(name, logPath="logs",
               formatter="[%(asctime)s] [%(pathname)s(line:%(lineno)d)] [%(levelname)s] %(message)s"):
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    handler = CyclonefwRotatingFileHandler("{}/{}.log".format(logPath, name), "a", 1024 * 1024 * 20, 10)
    handler.setFormatter(logging.Formatter(formatter))
    return handler


class CyclonefwRotatingFileHandler(RotatingFileHandler):
    def emit(self, record):
        if hasattr(record, "trace_id"):
            self.setFormatter(logging.Formatter("[%(asctime)s] [%(trace_id)s] [%(app_name)s] [%(pathname)s(line:%(lineno)d)] [%(levelname)s] %(message)s"))

        super(CyclonefwRotatingFileHandler, self).emit(record)


def register(consulServer, name, ip, port, tags):
    """
    注册到注册中心
    :param consulServer:
    :param name:
    :param ip:
    :param port:
    :param tags:
    :return:
    """
    data = {
        "name": name,
        "address": ip,
        "port": port,
        "tags": tags,
        "check": {}
    }
    try:
        requests.put("{}/v1/agent/service/register".format(consulServer), headers={
            "Content-Type": "application/json"
        }, data=json.dumps(data))
    except Exception as e:
        print(e)


def unregister(consulServer, name):
    """
    反注册到注册中心
    :param consulServer:
    :param name:
    :return:
    """
    try:
        requests.put("{}/v1/agent/service/deregister/{}".format(consulServer, name))
    except Exception as e:
        print(e)


def getHostnameAndIp():
    """
    获取hostname及ip地址
    :return: hostname, ip
    """
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return hostname, ip
