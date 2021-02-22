import asyncio
import sys
import time
import traceback
import warnings
from functools import wraps

# https://www.jianshu.com/p/ee82b941772a
import aiohttp.client_exceptions
import requests
from aiohttp import ClientProxyConnectionError

from re_common.baselibrary.utils.core.requests_core import MsgCode


def InterVal(start_time, interval):
    '''
    执行函数必须间隔多少时间,没有到指定的时间函数就不会被执行
    :param start_time: 传入开始时间
    :param interval: 秒数
    :return: 返回执行结果  否则返回 None
    '''

    def dewrapper(func):
        """
        它能把原函数的元信息拷贝到装饰器里面的 func 函数中。
        函数的元信息包括docstring、name、参数列表等等。可以尝试去除@functools.wraps(func)，
        你会发现test.__name__的输出变成了wrapper。
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = start_time
            time_now = int(time.time())
            if time_now - start > interval:
                result = func(*args, **kwargs)
                return result
            else:
                return None

        return wrapper

    return dewrapper


def timethis(func):
    """
    函数执行的时间差
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper


def try_except(callback=None, is_print=True):
    """
    使用装饰器使用try_except,并用callback回收错误信息
    :param func:
    :return:
    """

    def dewrapper(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseException as e:
                if callback is not None:
                    callback(*sys.exc_info(), *args, **kwargs)
                if is_print:
                    print(traceback.format_exc())
                return None

        return wrapper

    return dewrapper


# https://blog.csdn.net/qq_39314099/article/details/83822593
def deprecated(message):
    def deprecated_decorator(func):
        @wraps(func)
        def deprecated_func(*args, **kwargs):
            warnings.warn("{} is a deprecated function. {}".format(func.__name__, message),
                          category=DeprecationWarning,
                          stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)

        return deprecated_func

    return deprecated_decorator


def request_try_except(func):
    """
    拦截request请求错误
    :param func:
    :return:
    """

    @wraps(func)
    def wrapTheFunction(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ReadTimeout as e:
            dicts = {"code": MsgCode.TIME_OUT_ERROR,
                     "msg": "time out, {}".format(repr(e))}
            return False, dicts
        except requests.exceptions.ProxyError as e:
            dicts = {"code": MsgCode.PROXY_ERROR,
                     "msg": "proxy error, {}".format(repr(e))}
            return False, dicts
        except:
            dicts = {"code": MsgCode.ON_KNOW,
                     "msg": traceback.format_exc()}
            return False, dicts

    return wrapTheFunction


def aiohttp_try_except(func):
    """
    拦截aiohttp 异步请求错误
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapTheFunction(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ClientProxyConnectionError as e:
            dicts = {"code": MsgCode.PROXY_ERROR,
                     "msg": "proxy error, {}".format(repr(e))}
            return False, dicts
        except asyncio.exceptions.TimeoutError as e:
            dicts = {"code": MsgCode.TIME_OUT_ERROR,
                     "msg": "time out, {}".format(repr(e))}
            return False, dicts
        except aiohttp.client_exceptions.ClientPayloadError as e:
            dicts = {"code": MsgCode.PAYLOAD_ERROR,
                     "msg": "非法的压缩格式，错误的chunk编码，数据不足Content-length, {}".format(repr(e))}
            return False, dicts
        except Exception as e:
            dicts = {"code": MsgCode.ON_KNOW,
                     "msg": traceback.format_exc()}
            return False, dicts

    return wrapTheFunction


def mongodb_try_except(func):
    """
    拦截mongodb执行错误
    :param func:
    :return:
    """

    @wraps(func)
    async def wrapTheFunction(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            dict_ = {
                "status": "FAILED",
                "msg_code": MsgCode.NO_RESOURCE,
                "msg": "保存到数据库失败",
                "data": {"err": repr(e)}
            }
            return False, dict_

    return wrapTheFunction
