# -*- coding:UTF-8 -*-
# 作者: l0n0l
# 时间: 2020/09/22 周二
# 点: 18:00:25

# 描述:异步 http 服务器

from aiohttp import web
import time
import asyncio
import signal
import logging
import traceback


class http_server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.update_list = []
        self.async_update_list = []
        self.update_elapse = 0.1
        self.running = True
        self.router = self.app.router
        self.add_route = self.app.router.add_route
        self.add_routes = self.app.router.add_routes
        self.add_static = self.app.router.add_static

    async def common_run(self):
        """启动服务器（用于与其他需要循环的架构融合)

        实现了一个死循环来执行其他框架的循环。
        通过add_update_func和add_async_update_func可以向循环中添加函数。
        """
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host=self.host, port=self.port)
        await site.start()
        cost = 0

        def on_signal():
            print("Stoping site ...")
            self.running = False

        try:
            loop = asyncio.get_event_loop()
            for signame in ('SIGINT', 'SIGTERM', 'SIGQUIT'):
                loop.add_signal_handler(getattr(signal, signame), on_signal)
        except NotImplementedError:
            pass

        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Server start at {self.host}:{self.port} at {start_time}")

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
        """
        启动服务器
        """
        web.run_app(self.app, host=self.host, port=self.port)

    def add_update_func(self, f):
        """向主循环添加同步更新函数(必须使用 common_run 启动服务器)

        @f:function: 有一个float参数表示主循环耗费的时间

        例如：
        ```
        server = http_server(host,port)
        def testf(cost):
            pass
        server.add_update_func(testf)
        ```
        """
        self.update_list.append(f)

    def add_async_update_func(self, f):
        """向主循环添加异步更新函数(必须使用 common_run 启动服务器)
        @f:function: 有一个float参数表示主循环耗费的时间

        例如：
        ```
        server = http_server(host,port)
        def testf(cost):
            pass
        server.add_update_func(testf)
        ```
        """
        self.async_update_list.append(f)

    def default_cos_header(self):
        """
        返回默认跨站header
        """
        return {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "*"
        }

    def route(self, method, path, option_headers=None):
        """装饰器,将异步函数装饰为访问route.

        @method: str : (get|post|put|delete|option)\n
        @path: str : "/a" "/{prefix}/a" "/a/b/c"\n
        @option_headers: (True | http header:dict) 会自动添加一个option方法的回调。
            如果option_header=True 会自动添加 default_cos_header 函数返回的默认跨站 option 方法。
            如果option_header={"header":value},会将dict中的header作为 option 方法返回的header\n

        例如：
        ```
        server = http_server(host,port)

        #1 添加 /test 路径
        @server.route("get", "/test")
        async def test_route(req)
            pass
        #2 添加 /任意值/test 路径，对于nginx反向代理很有用
        @server.route("get", "/{prefix}/test")
        async def test_route(req)
            pass
        
        #3 添加 默认的跨站option方法
        @server.route("get", "/{prefix}/test", server.default_cos_header())
        async def test_route(req)
            pass

        #4 添加 默认的跨站option方法
        @server.route("get", "/{prefix}/test", True)
        async def test_route(req)
            pass
        ```
        例3 和 例4 是等价的
        """
        def f(func):
            oh = option_headers
            self.add_route(method, path, func)
            if oh is not None:
                if isinstance(oh, bool) and oh == True:
                    oh = self.default_cos_header()

                async def option_handler(request: web.Request):
                    return web.Response(headers=oh)

                self.app.router.add_options(path, option_handler)
            return func
        return f
