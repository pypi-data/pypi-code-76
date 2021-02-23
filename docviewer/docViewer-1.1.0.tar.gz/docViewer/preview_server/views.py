import asyncio

import tornado.web
import tornado.websocket


class IndexHandler(tornado.web.RequestHandler):
    async def get(self):
        await asyncio.sleep(2)
        self.write('hello')


class LitePreview(tornado.websocket.WebSocketHandler):
    pass
