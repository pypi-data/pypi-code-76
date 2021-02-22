from confluent_kafka.cimpl import Producer
from mobio.libs.kafka_lib import KAFKA_BOOTSTRAP


class KafkaConfluent(object):
    # Here will be the instance stored.
    _instance = None

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            # cls._instance = cls.__new__(cls)
            cls._instance = Producer(
                {
                    "request.timeout.ms": 20000,
                    "bootstrap.servers": KAFKA_BOOTSTRAP,
                }
            )
        return cls._instance


class ConfluentProducerManager:
    @staticmethod
    def send_message_to_topic_without_flush(topic: str, data):
        KafkaConfluent.instance().produce(topic, data)
        print("topic: {}, message: {}".format(topic, data))

    @staticmethod
    def flush_to_topic():
        KafkaConfluent.instance().poll(0)
        KafkaConfluent.instance().flush()

    @staticmethod
    def send_message_to_topic(topic: str, data):
        KafkaConfluent.instance().produce(topic, data)
        KafkaConfluent.instance().poll(0)
        print("topic: {}, message: {}".format(topic, data))
        KafkaConfluent.instance().flush()

    @staticmethod
    def send_message_to_topic_with_key(topic: str, key: str, data):
        KafkaConfluent.instance().produce(topic=topic, value=data, key=key.encode())
        KafkaConfluent.instance().poll(0)
        print("topic: {}, message: {}".format(topic, data))
        KafkaConfluent.instance().flush()

    @staticmethod
    def send_message_to_topic_with_key_without_flush(topic: str, key: str, data):
        KafkaConfluent.instance().produce(topic=topic, value=data, key=key.encode())
        print("topic: {}, message: {}".format(topic, data))


if __name__ == "__main__":
    topic_name = "test"
    for i in range(1000):
        ConfluentProducerManager.send_message_to_topic(topic=topic_name, data=str(i))
    ConfluentProducerManager.flush_to_topic()
