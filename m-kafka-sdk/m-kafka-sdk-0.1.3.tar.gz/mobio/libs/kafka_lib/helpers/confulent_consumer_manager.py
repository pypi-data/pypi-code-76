import json
import uuid
from copy import deepcopy
from datetime import datetime, timedelta
from threading import Thread
import threading
from abc import abstractmethod
from time import time
from confluent_kafka.cimpl import KafkaError, KafkaException
from confluent_kafka import Consumer

from mobio.libs.kafka_lib import ConsumerGroup, KAFKA_BOOTSTRAP, RequeueStatus
from mobio.libs.kafka_lib.models.mongo.requeue_consumer_model import (
    RequeueConsumerModel,
)


class ConfluentThreadConsumer(Thread):
    def __init__(self, t_id, func, *args):
        super().__init__()
        self.args = args
        self.func = func
        self.id = t_id
        # self.daemon = True

    def run(self):
        self.func(*self.args)

    def __del__(self):
        print("ThreadConsumer: __del__: ok")


class ConfluentConsumerManager:
    def __init__(self, consumer_list):
        # self.arr_workers = Queue(64)
        self.consumer_list = consumer_list
        self.arr_workers = []

        self.init_manager()

    def init_manager(self):
        for cls, client_mongo, topic, worker, group_id, retryable in self.consumer_list:
            self.init_consumer(cls, client_mongo, topic, worker, group_id, retryable)

    def init_consumer(self, cls, client_mongo, topic, num_worker, group_id, retryable):
        consumer = cls(client_mongo, topic, num_worker, group_id, retryable)
        self.arr_workers.append(consumer)
        # self.arr_workers.put(consumer)

    def __del__(self):
        print("ConsumerManager: __del__: ok")


class ConfluentMessageQueue:
    MIN_COMMIT_COUNT = 10

    def __init__(
        self,
        client_mongo,
        topic_name,
        num_worker,
        group_id=ConsumerGroup.DEFAULT_CONSUMER_GROUP_ID,
        retryable=True,
    ):
        if not group_id:
            group_id = ConsumerGroup.DEFAULT_CONSUMER_GROUP_ID
        self.num_worker = num_worker
        self.topic_name = topic_name
        self.group_id = group_id
        self.client_mongo = client_mongo
        self.thread = []
        self.retryable = retryable

        self.stop_event = threading.Event()
        for i in range(num_worker):
            t = ConfluentThreadConsumer(i, self.on_process)
            self.thread += [t]
            t.start()

    def on_process(self):
        print("KafkaPythonMessageQueue: on_process")
        consumer = Consumer(
            {
                "bootstrap.servers": KAFKA_BOOTSTRAP,
                "group.id": self.group_id,
                "auto.offset.reset": "latest",
            }
        )
        try:
            consumer.subscribe([self.topic_name])

            msg_count = 0
            while not self.stop_event.is_set():
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        print(
                            "%% %s [%d] reached end at offset %d\n"
                            % (msg.topic(), msg.partition(), msg.offset())
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    count_err = 0
                    data = None
                    key = msg.key()
                    try:
                        data = None
                        message = msg.value().decode("utf-8")
                        payload = json.loads(message)
                        data = deepcopy(payload)
                        if "message_id" in payload and type(payload) == dict:
                            message_id = payload.pop("message_id")
                        else:
                            message_id = str(uuid.uuid4())
                        if "count_err" in payload:
                            count_err = payload.pop("count_err")
                        start_time = time()
                        print(
                            "start: {} with message_id: {} start_time: {}".format(
                                self.topic_name, message_id, start_time
                            )
                        )
                        self.process_msg(payload)
                        msg_count += 1
                        if msg_count % self.MIN_COMMIT_COUNT == 0:
                            consumer.commit(async=True)
                        end_time = time()
                        print(
                            "end: {} with message_id: {} total time: '[{:.3f}s]".format(
                                self.topic_name, message_id, end_time - start_time
                            )
                        )
                    except Exception as e:
                        print(
                            "MessageQueue::run - topic: {} ERR: {}".format(
                                self.topic_name, e
                            )
                        )
                        if data and self.retryable:
                            data_error = {
                                "topic": self.topic_name,
                                "key": key.decode('ascii') if key else key,
                                "data": data,
                                "error": str(e),
                                "count_err": count_err + 1,
                                "next_run": datetime.utcnow() + timedelta(minutes=5),
                                "status": RequeueStatus.ENABLE
                                if (count_err + 1) <= 10
                                else RequeueStatus.DISABLE,
                            }
                            result = RequeueConsumerModel(self.client_mongo).insert(
                                data=data_error
                            )
                            print("RequeueConsumerModel result: {}".format(result))

        finally:
            # Close down consumer to commit final offsets.
            consumer.close()

    def start_consumer(self):
        print("MessageQueue: start_consumer")
        for t in self.thread:
            t.join()
        print("ok")

    @abstractmethod
    def process_msg(self, payload):
        raise NotImplementedError("You must implement this function on child class")

    def __del__(self):
        print("MessageQueue: __del__")
