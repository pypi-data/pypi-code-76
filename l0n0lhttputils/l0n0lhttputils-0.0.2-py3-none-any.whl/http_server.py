# -*- coding:UTF-8 -*-
# 作者: l0n0l
# 时间: 2020/09/22 周二
# 点: 18:00:25

# 描述:异步 http 服务器

from aiohttp import web
import time
import asyncio
import signal


class http_server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.update_list = []
        self.async_update_list = []
        self.update_elapse = 0.1
        self.running = True
        self.routes = web.RouteTableDef()

    def add_route(self, method, path, handler):
        self.app.router.add_route(method, path, handler)

    def add_routes(self, routes):
        self.app.router.add_routes(routes)

    async def common_run(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host=self.host, port=self.port)
        await site.start()
        cost = 0

        def on_signal():
            print("Stoping site ...")
            self.running = False

        loop = asyncio.get_event_loop()
        for signame in ('SIGINT', 'SIGTERM', 'SIGQUIT'):
            loop.add_signal_handler(getattr(signal, signame), on_signal)

        while self.running:
            pre = time.time()
            for f in self.update_list:
                f(cost)
            for f in self.async_update_list:
                await f(cost)
            cost = time.time() - pre
            if cost < self.update_elapse:
                await asyncio.sleep(self.update_elapse - cost)
                cost = self.update_elapse

        await site.stop()

    def run(self):
        web.run_app(self.app, host=self.host, port=self.port)

    def add_update_func(self, f):
        self.update_list.append(f)

    def add_async_update_func(self, f):
        self.async_update_list.append(f)
