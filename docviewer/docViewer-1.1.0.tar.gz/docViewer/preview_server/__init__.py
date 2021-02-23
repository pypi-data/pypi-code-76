import asyncio
import logging
import time

import tornado.ioloop
import tornado.web

from . import config, urls

logger = logging.getLogger('docViewer.server')


def make_app(**kwargs):
    kwargs.setdefault('DOC_ROOT', config.DOC_ROOT)
    application = tornado.web.Application(
        urls.urlpatterns,
        template_path=config.TEMPLATE_DIR,
        **kwargs,
    )
    return application


async def close_when_idle(server=None, wait_before=20):
    idle_since = None
    while True:
        await asyncio.sleep(1)
        if server._connections:
            continue
        if idle_since:
            idle_time = time.time() - idle_since
            if idle_time > wait_before:
                server.stop()
                ioloop = tornado.ioloop.IOLoop.current()
                ioloop.add_callback(ioloop.stop)
                logger.info('[idle_time: %s] now stop server', idle_time)
        else:
            idle_since = time.time()
