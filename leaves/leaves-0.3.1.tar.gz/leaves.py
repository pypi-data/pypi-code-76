"""
Author:     LanHao
Date:       2021/2/8 10:27
Python:     python3.6

"""
import json
import uuid
import traceback
import asyncio
import logging
from typing import List, Union

import aio_pika
import aiormq
from pamqp import specification as spec

logger = logging.getLogger(__name__)


# 生产者端调用接收

class Service(object):
    name: str = None
    connection: aio_pika.connection.Connection = None

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
    connection: aio_pika.connection.Connection = None
    channel: aio_pika.channel.Channel = None
    service: Service = None
    future = None

    async def on_callback(self, message: aio_pika.IncomingMessage):
        """
        等待异步的结果
        :param message:
        :return:
        """
        logger.debug(f"接受到回调消息:{json.loads(message.body)}")
        with message.process():
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
        async with self.channel:
            queue = await self.channel.declare_queue(f"leaves_{self.name}_{correlation_id}", exclusive=True)
            logger.debug(f"建立结果监听队列:{queue}")

            await queue.consume(self.on_callback)  # 注册函数而非一直等待

            data = {"args": args, "kwargs": kwargs}
            self.future = asyncio.get_event_loop().create_future()

            logger.debug(f"准备向交换机:{self.service.name} 下 {self.name} 队列,发送数据:{data}")

            direct_exchange = await self.channel.declare_exchange(
                self.service.name, aio_pika.ExchangeType.DIRECT
            )

            await direct_exchange.publish(
                aio_pika.Message(
                    json.dumps(data).encode(),
                    correlation_id=correlation_id,
                    reply_to=queue.name
                ),
                routing_key=self.name,
            )

            back = await self.future

        if back["status"]:
            return back["result"]
        else:
            logger.error(f"执行结果发生异常:{back}")
            raise Exception(back["result"])


class RPC(object):
    """
    顶层rpc 调用,供客户端使用

    支持从外部传入connection,为后续做连接池防止并发导致的大量链接做准备
    """

    con_url: Union[str, aiormq.connection.Connection] = ""
    connection: aio_pika.connection.Connection = None

    def __init__(self, con_url: Union[str, aiormq.connection.Connection]):
        self.con_url = con_url

    async def __aenter__(self):
        if isinstance(self.con_url, str):
            self.connection = await aio_pika.connect(self.con_url)
        else:
            self.connection = self.con_url
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self.con_url, str):
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
    con_url: str
    _connection: aio_pika.connection.Connection

    def __init__(self, name: str):
        self.name = name
        self.leaves = []  # 存放所有的树叶
        self.con_url = ""

    def leaf(self, *args, **kwargs):
        _leaf = Leaf(self, *args, **kwargs)

        return _leaf.registe_func

    async def start(self, con_url: str):
        """
        去让所有的叶片开始队列监听功能
        :param con_url:
        :return:
        """

        self._connection = await aio_pika.connect_robust(con_url)  # 此种用法支持自动重连并注册函数

        for leaf in self.leaves:
            leaf: Leaf
            leaf.connection = self._connection
            asyncio.ensure_future(leaf.start())


class Leaf(object):
    """
    单个用于存放处理函数的叶片
    """
    branch: Branch = None
    connection: aio_pika.connection.Connection = None
    func = None
    prefetch_count: int
    timeout: int = None

    def __init__(self, branch: Branch, prefetch_count: int = 1, timeout: int = None, *args, **kwargs):
        self.branch = branch
        self.prefetch_count = prefetch_count
        self.timeout = timeout

    async def on_response(self, message: aio_pika.IncomingMessage):

        logger.debug(f"即将调用函数:{self.branch.name}.{self.func.__name__}:{message.body}")

        with message.process():
            body = {}
            try:
                body = json.loads(message.body)
            except Exception as e:
                logger.error(f"数据接收异常,无法正常转换json，{e},{message.body}")

            args = body.get("args", [])
            kwargs = body.get("kwargs", {})
            status = True
            try:
                data = await asyncio.wait_for(self.func(*args, **kwargs), timeout=self.timeout)
            except asyncio.TimeoutError:
                data = "计算超时"
                status = False
            except Exception as e:
                logger.error(f"执行函数{self.func.__name__}时发生错误:{e},{traceback.format_exc()}")
                data = f"{e}"
                status = False

            back_data = {
                "status": status,
                "result": data
            }

            if message.reply_to:
                try:
                    await message.channel.basic_publish(
                        body=json.dumps(back_data).encode(),
                        routing_key=message.reply_to,
                        properties=spec.Basic.Properties(
                            correlation_id=message.correlation_id
                        )
                    )
                    logger.debug(f"成功向队列:{message.reply_to} 回发任务结果,"
                                 f"correlation_id:{message.correlation_id}")
                except Exception as e:
                    logger.error(f"回发任务时发生错误：{e},\r\n {traceback.format_exc()}")
                    raise e
            else:
                logger.warning(f"未指定rpc 任务回发队列,将不进行结果回传")

            logger.debug(f"执行完毕:{self.branch.name}.{self.func.__name__}")
        logger.debug(f"消息ack:{self.branch.name}.{self.func.__name__}")

    def registe_func(self, func):
        self.func = func

        self.branch.leaves.append(self)

        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    async def start(self):
        """
        让每个叶片都独立起飞？
        :return:
        """
        logger.debug(f"监听:exchanges:{self.branch.name},queue:{self.func.__name__}")
        channel: aio_pika.channel.Channel = await self.connection.channel()
        await channel.set_qos(prefetch_count=self.prefetch_count)

        direct_logs_exchange = await channel.declare_exchange(
            self.branch.name, aio_pika.ExchangeType.DIRECT
        )
        queue = await channel.declare_queue(self.func.__name__, durable=True)  # 队列需要持久化用于接受所有的任务
        await queue.bind(direct_logs_exchange, routing_key=self.func.__name__)

        await queue.consume(self.on_response)


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
