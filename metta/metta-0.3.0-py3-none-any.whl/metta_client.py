import asyncio
import uvloop

from typing import Iterable, List, Type
from multiprocessing import Process

from metta.nodes.node import Node
from metta.common.topics import ProtobufMessage, TopicRegistry, Topic


class MettaClient:
    def __init__(self, *, kafka_brokers: List[str], zookeeper_hosts: List[str]) -> None:
        self.kafka_brokers = kafka_brokers
        self.zookeeper_hosts = zookeeper_hosts

        self.nodes: List[Node] = []
        self.processes: List[Process] = []

    def add_node(self, *nodes: Node):
        for node in nodes:
            self.nodes.append(node)

    def run(self, start_ts, end_ts, profile):
        def process(node: Node):
            async def exec(n):
                async with n:
                    await n.run(start_ts, end_ts, profile)

            uvloop.install()
            asyncio.run(exec(node))

        if len(self.processes > 0):
            raise RuntimeError("Nodes are already running.")

        self.processes = []
        for node in self.nodes:
            for _ in range(node.replicas):
                p = Process(target=process, args=(node))
                p.start()
                self.processes.append(p)

        for p in self.processes:
            p.join()

    def stop(self):
        for p in self.processes:
            p.terminate()

    def register_topics(self, *topics: Iterable[Topic]):
        async def _register():
            async with TopicRegistry(
                kafka_brokers=self.kafka_brokers, zookeeper_hosts=self.zookeeper_hosts
            ) as topic_registry:
                for topic in topics:
                    await topic_registry.register(topic)

        asyncio.run(_register())
