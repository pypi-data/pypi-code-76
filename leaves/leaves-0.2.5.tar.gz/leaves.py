"""
Author:     LanHao
Date:       2021/2/8 10:27
Python:     python3.6

"""
import json
import uuid
import asyncio
import logging
from typing import List

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
class Branch(object):
    """

    寓意为树枝,其上可以拥有多个树叶,每个树叶当表示一个函数调用

    一个树枝内的树叶将共用一个tcp链接,基于不同的channel实现

    所以对于任务的并发,可以通过leaf的设置实现，是基于单个函数的控制实现的

    """

    name: str = ""
    leaves: List

    def __init__(self, name: str):
        self.name = name
        self.leaves = []  # 存放所有的树叶

    def leaf(self, *args, **kwargs):
        _leaf = Leaf(self, *args, **kwargs)

        return _leaf.registe_func

    async def start(self, con_url: str):
        """
        去让所有的叶片开始队列监听功能
        :param con_url:
        :return:
        """

        connection = await aiormq.connect(con_url)
        for leaf in self.leaves:
            leaf: Leaf
            leaf.connection = connection
            await leaf.start()


class Leaf(object):
    """
    单个用于存放处理函数的叶片
    """
    branch: Branch = None
    connection = None
    func = None
    prefetch_count: int
    timeout: int = None

    def __init__(self, branch: Branch, prefetch_count: int = 1, timeout: int = None, *args, **kwargs):
        self.branch = branch
        self.prefetch_count = prefetch_count
        self.timeout = timeout

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
        if message.header.properties.reply_to:
            try:
                await message.channel.basic_publish(
                    json.dumps(back_data).encode(),
                    routing_key=message.header.properties.reply_to,
                    properties=aiormq.spec.Basic.Properties(
                        correlation_id=message.header.properties.correlation_id
                    ),
                )
            except Exception as e:
                logger.error(f"回发任务时发生错误：{e}")

        await message.channel.basic_ack(message.delivery.delivery_tag)  # 确定回发成功后,再执行ack

    async def on_response(self, message: aiormq.types.DeliveredMessage):
        logger.debug(f"接收任务并即将调用函数:{self.branch.name}.{self.func.__name__}")
        await self.call_back(message, self.func)
        logger.debug(f"执行完毕:{self.branch.name}.{self.func.__name__}")

    def registe_func(self, func):
        self.func = func

        # self.branch.leaves[func_name] = self.on_response
        self.branch.leaves.append(self)

        async def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    async def start(self):
        """
        让每个叶片都独立起飞？
        :return:
        """
        logger.debug(f"监听:exchanges:{self.branch.name},queue:{self.func.__name__}")
        channel = await self.connection.channel()
        await channel.basic_qos(prefetch_count=self.prefetch_count)  # 限制同时接受的任务数
        await channel.exchange_declare(exchange=self.branch.name)
        declare_ok = await channel.queue_declare(self.func.__name__, durable=True)  # 队列需要持久化用于接受所有的任务
        await channel.queue_bind(exchange=self.branch.name, routing_key=self.func.__name__, queue=self.func.__name__)
        await channel.basic_consume(declare_ok.queue, self.on_response)


class MicroContainer(object):
    """

    单个节点运行的容器

    """
    branchs: List[Branch] = None
    con_url: str = ""

    def __init__(self, branchs: List[Branch], con_url: str):
        self.branchs = branchs
        self.con_url = con_url

    async def service_publish(self):
        """
        关于初始化任务监听部分的工作,可以定制
        :return:
        """
        for branch in self.branchs:
            branch: Branch
            await branch.start(self.con_url)

    def run(self):
        asyncio.ensure_future(self.service_publish())
        asyncio.get_event_loop().run_forever()
