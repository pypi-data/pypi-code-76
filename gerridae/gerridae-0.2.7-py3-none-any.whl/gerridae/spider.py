import asyncio
from datetime import datetime

import aiohttp

from .log import get_logger
from .request import Request, Response

logger = get_logger(__name__)

HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KH"
                  "TML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


class Spider:
    def __init__(self):
        pass

    start_urls = []
    encoding = None
    name = 'Spider'
    sender = 0
    returned = 0

    @staticmethod
    def is_crawl(url):
        return False

    def parse(self, rep):
        raise NotImplementedError

    @classmethod
    async def start(cls):
        logger.info(f'{cls.name} Start Crawl')
        start_time, spider_ins = datetime.now(), cls()

        if isinstance(spider_ins.start_urls, str):
            spider_ins.start_urls = [spider_ins.start_urls]

        async with aiohttp.ClientSession() as session:
            loop = asyncio.get_running_loop()
            loop.set_debug(True)
            logger.info(f'start create task except create {len(spider_ins.start_urls)} task')
            tasks = [asyncio.create_task(spider_ins.request(url, session=session)) for url in spider_ins.start_urls if
                     not spider_ins.is_crawl(url)]
            logger.info(f'already create  {len(tasks)} tasks')
            finished, unfinished = await asyncio.wait(tasks)
            logger.info(f'fail task num: {len(unfinished)}')
            data = [r.result() for r in finished]
            logger.info(f"{cls.name} cost time {datetime.now() - start_time}")
            return data

    async def request(self, url, *, session=None) -> Response:
        resp = await Request(url, request_session=session).fetch()
        return await self.parse(resp)
