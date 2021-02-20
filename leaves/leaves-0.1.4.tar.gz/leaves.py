"""
Author:     LanHao
Date:       2021/2/8 10:27
Python:     python3.6

"""
import json
import uuid
import asyncio
import logging
import multiprocessing
import concurrent.futures
from typing import Dict, List

import aiormq
import pamqp

logger = logging.getLogger(__name__)


# 生产者端调用接收

class Service(object):
    name: str = None
    connection: aiormq.connection.Connection = None

    def __getattr__(self, item):
        method = Method()
        method.name = item
        method.connection = self.connection
        method.service = self
        return method


class Method(object):
    """
    rpc 调用端使用
    """
    name: str = None
    connection: aiormq.connection.Connection = None
    channel: aiormq.channel.Channel = None
    service: Service = None
    future = None

    async def on_callback(self, message: aiormq.types.DeliveredMessage):
        """
        等待异步的结果
        :param message:
        :return:
        """
        try:
            await message.channel.basic_ack(message.delivery.delivery_tag)
        except Exception as e:
            logger.error(f"等待结果后ack 消息时失败:{e}")

        self.future.set_result(json.loads(message.body))

    async def __call__(self, *args, **kwargs):
        """
        异步调用
        :param args:
        :param kwargs:
        :return:
        """

        correlation_id = str(uuid.uuid4())  # 随机ID

        self.channel = await self.connection.channel()  # 每次调用都将复用connection 新建channel
        declare_ok: pamqp.commands.Queue.DeclareOk = await self.channel.queue_declare(
            f"leaves_{self.name}_{correlation_id}",
            exclusive=True,  # auto_delete=True, # exclusive已经将自动删除
        )

        await self.channel.basic_consume(declare_ok.queue, self.on_callback)

        data = {"args": args, "kwargs": kwargs}

        self.future = asyncio.get_event_loop().create_future()

        await self.channel.basic_publish(
            json.dumps(data).encode(),
            exchange=self.service.name,
            routing_key=self.name,
            properties=aiormq.spec.Basic.Properties(
                content_type='text/plain',
                correlation_id=correlation_id,
                reply_to=declare_ok.queue,
            )
        )  # 结果接受队列创建完毕后再发布任务

        back = await self.future

        await self.channel.close()  # 关闭channel 并将删除独占的队列

        if back["status"]:
            return back["result"]
        else:
            logger.error(f"执行结果发生异常:{back}")
            raise Exception(back["result"])


class RPC(object):
    """
    顶层rpc 调用,供客户端使用
    """

    con_url: str = ""
    connection: aiormq.connection.Connection = None

    def __init__(self, con_url: str):
        self.con_url = con_url

    async def __aenter__(self):
        self.connection = await aiormq.connect(self.con_url)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()

    def __getattr__(self, item):
        server = Service()
        server.name = item
        server.connection = self.connection
        return server


# 消费者端发布


class Leaf(object):
    """
    单个用于存放处理函数的叶片
    """

    name: str = None
    method: Dict = None

    def __init__(self, name: str):
        self.name = name
        self.method = {}

    def rpc(self, *args, **kwargs):
        texture = Texture(self, *args, **kwargs)
        return texture.register


class Texture(object):
    """

    单个函数的注册

    """
    leaf: Leaf = None
    func = None
    timeout: int = None

    def __init__(self, leaf: Leaf, timeout: int = None):
        self.leaf = leaf
        self.timeout = timeout

    async def on_response(self, message: aiormq.types.DeliveredMessage):
        await self.call_back(message, self.func)

    def register(self, func):
        func_name = func.__name__
        self.func = func
        self.leaf.method[func_name] = self.on_response

        async def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    async def call_back(self, message: aiormq.types.DeliveredMessage, func):
        """
        常规调用，未增加新开线程or 进程调用
        :param message:
        :param func:
        :return:
        """

        body = json.loads(message.body)
        args = body["args"]
        kwargs = body["kwargs"]
        data = None
        status = True
        try:
            data = await asyncio.wait_for(func(*args, **kwargs), timeout=self.timeout)
        except asyncio.TimeoutError:
            data = "计算超时"
            status = False

        except Exception as e:
            logger.error(f"执行函数{func.__name__}时发生错误:{e}")
            data = f"{e}"
            status = False

        back_data = {
            "status": status,
            "result": data
        }

        await message.channel.basic_ack(message.delivery.delivery_tag)

        await message.channel.basic_publish(
            json.dumps(back_data).encode(),
            routing_key=message.header.properties.reply_to,
            properties=aiormq.spec.Basic.Properties(
                correlation_id=message.header.properties.correlation_id
            ),
        )


class MicroContainer(object):
    """

    单个节点运行的容器

    """
    leaves: List[Leaf] = None
    con_url: str = ""
    prefetch_count: int = 1

    def __init__(self, leaves: List[Leaf], con_url: str, prefetch_count: int = 1, executor=None):
        self.leaves = leaves
        self.con_url = con_url
        self.prefetch_count = prefetch_count
        if executor is None:
            max_workers = max(multiprocessing.cpu_count() - 1, 1)
            logger.info(f"loop default executor max_workers:{max_workers}")
            executor = concurrent.futures.ProcessPoolExecutor(max_workers=max_workers)
        loop = asyncio.get_event_loop()
        loop.set_default_executor(executor)

    async def service_publish(self):
        """
        关于初始化任务监听部分的工作,可以定制
        :param container:
        :return:
        """

        connection = await aiormq.connect(self.con_url)
        channel = await connection.channel()
        await channel.basic_qos(prefetch_count=self.prefetch_count)  # 限制同时接受的任务数
        # 发布任务端核定,exchange 和 queue 都不应该断开链接自动删除
        for leaf in self.leaves:
            leaf: Leaf
            await channel.exchange_declare(exchange=leaf.name)
            for key, func in leaf.method.items():
                declare_ok = await channel.queue_declare(key, durable=True)  # 队列需要持久化用于接受所有的任务
                await channel.queue_bind(exchange=leaf.name, routing_key=key, queue=key)
                await channel.basic_consume(declare_ok.queue, func)
