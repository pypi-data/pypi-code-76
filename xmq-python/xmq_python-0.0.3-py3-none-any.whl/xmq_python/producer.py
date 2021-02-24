from .adapters.producer_amqp import ProducerAMQP
from .mq_type import *


class Producer(object):
    def __init__(self, mq_type='AMQO', producer_group_id='', lookup_address='', node_address='', access_key='', access_secret='', timeout=None, max_message_size=None, username=None, password=None, **config):
        if mq_type == MQ_TYPE_AMQP:
            self.__agent = ProducerAMQP(producer_group_id=producer_group_id, lookup_address=lookup_address,
                                        node_address=node_address, access_key=access_key, access_secret=access_secret, **config)
        else:
            self.__agent = ProducerAMQP(producer_group_id=producer_group_id, lookup_address=lookup_address,
                                        node_address=node_address, access_key=access_key, access_secret=access_secret, **config)

    def Start(self):
        self.__agent.Start()

    def Stop(self):
        self.__agent.Stop()

    def Publish(self, topic_group: str, topic: str, message, **route):
        return self.__agent.Publish(topic_group, topic, message, **route)

    def DelayPublish(self, topic_group: str, topic: str, delay: int, message, **route):
        return self.__agent.DelayPublish(topic_group, topic, delay, message, **route)
