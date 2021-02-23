import asyncio
from functools import partial
from helper import async_retry, to_async


def test(a=1):
    print(a)



asyncio.run(async_retry(partial(to_async, test, a=1)))