from .adapters.comsumer_amqp import ComsumerAMQP
from .mq_type import *


class Comsumer(object):
    def __init__(self, mq_type='AMQP', comsumer_group_id='', lookup_address='', node_address='', access_key='', access_secret='', thread_num=None, batch_size=None, username=None, password=None, **config):
        if mq_type == MQ_TYPE_AMQP:
            self.__agent = ComsumerAMQP(comsumer_group_id=comsumer_group_id, lookup_address=lookup_address,
                                        node_address=node_address, access_key=access_key, access_secret=access_secret, thread_num=thread_num, batch_size=batch_size, username=username, password=password, **config)
        else:
            self.__agent = ComsumerAMQP(comsumer_group_id=comsumer_group_id, lookup_address=lookup_address,
                                        node_address=node_address, access_key=access_key, access_secret=access_secret, thread_num=thread_num, batch_size=batch_size, username=username, password=password, **config)

    def Register(self, topic_group: str, topic: str, callback, **route):
        self.__agent.Register(topic_group, topic, callback, **route)

    def Start(self):
        self.__agent.Start()

    def Stop(self):
        self.__agent.Stop()
