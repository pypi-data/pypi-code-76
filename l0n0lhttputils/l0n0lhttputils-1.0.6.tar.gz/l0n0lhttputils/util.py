import hashlib
import random
import string
from aiohttp.web import Request


def md5(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()


def random_string(slen=10):
    return ''.join(random.sample(string.ascii_letters + string.digits + '!@#$%^&*()_+=-', slen))


async def get_multipart(request: Request) -> dict:
    """
    读取mutipart
        @request:http请求
        @return:返回multipart的字典
    """
    ret = {}
    fdata = await request.multipart()
    while True:
        d = await fdata.next()
        if d is None:
            break
        ret[d.name] = await d.read()

    return ret


def ok(data: dict):
    return "OK" == data["errMsg"] \
        or "Ok" == data["errMsg"] \
        or "oK" == data["errMsg"] \
        or "ok" == data["errMsg"]
