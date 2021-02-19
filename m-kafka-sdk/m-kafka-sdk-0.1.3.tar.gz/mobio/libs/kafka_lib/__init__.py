import os


class ConsumerGroup:
    DEFAULT_CONSUMER_GROUP_ID = "mobio-consumers"


class RequeueStatus:
    ENABLE = 0
    DISABLE = -1


class MobioEnvironment:
    HOST = 'HOST'
    ADMIN_HOST = 'ADMIN_HOST'
    REDIS_URI = 'REDIS_URI'
    REDIS_HOST = 'REDIS_HOST'
    REDIS_PORT = 'REDIS_PORT'
    KAFKA_BROKER = 'KAFKA_BROKER'
    KAFKA_REPLICATION_FACTOR = 'KAFKA_REPLICATION_FACTOR'


KAFKA_BOOTSTRAP = os.getenv(MobioEnvironment.KAFKA_BROKER)
