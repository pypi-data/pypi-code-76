from typing import Any
import asyncio, logging
from functools import partial
from datetime import datetime
import random, string, hashlib, json, datetime, time


def singleton(cls):
    """ 单例模式 """
    instances = dict()

    def inner(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return inner


def random_str(length: int) -> str:
    seed = string.digits + string.ascii_letters
    return ''.join(random.choices(seed, k=length))


def md5(_str: str):
    return hashlib.md5(_str.encode()).hexdigest()


def json_encoder(obj: Any):
    """ JSON 序列化, 修复时间 """
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    return super().default(obj)


def json_decoder(obj: Any):
    """ JSON 反序列化，加载时间 """
    ret = obj
    if isinstance(obj, list):
        obj = enumerate(obj)
    elif isinstance(obj, dict):
        obj = obj.items()
    else:
        return obj

    for key, item in obj:
        if isinstance(item, (list, dict)):
            ret[key] = json_decoder(item)
        elif isinstance(item, str):
            try:
                ret[key] = datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                ret[key] = item
        else:
            ret[key] = item
    return ret


def json_friendly_loads(obj: Any):
    return json.loads(obj, object_hook=json_decoder)


def json_friendly_dumps(obj: Any, **kwargs):
    return json.dumps(obj, ensure_ascii=False, default=json_encoder, **kwargs)


def retry(f, times=2, interval=0):
    """
    from functools import partial
    f = partial(test, *args, **kwargs)
    """
    try:
        return f()
    except Exception as e:
        if times > 0:
            if interval > 0:
                time.sleep(interval)
            return retry(f, times=times - 1, interval=interval)
        raise e


async def async_retry(f, times=2, interval=0):
    """
    from functools import partial
    f = partial(test, *args, **kwargs)
    """
    try:
        return await f()
    except Exception as e:
        if times > 0:
            if interval > 0:
                await asyncio.sleep(interval)
            return await async_retry(f, times=times - 1, interval=interval)
        raise e


def asynio_loop():
    loop = asyncio.get_event_loop()
    if not loop:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop=loop)
    return loop


async def to_async(f, *args, **kwargs):
    try:
        return await asynio_loop().run_in_executor(None, partial(f, *args, **kwargs))
    except Exception as e:
        logging.exception('to_async:' + str(datetime.now()), exc_info=e)
