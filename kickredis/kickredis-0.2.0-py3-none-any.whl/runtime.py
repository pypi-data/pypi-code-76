from lightbus.transports.redis.event import RedisEventTransport, StreamUse

from kickredis.registry import ObjectRegistry, Stream
from kickredis.config import kicker_config


class KickerRuntime:
    def __init__(self):
        self._event_transport = RedisEventTransport(
            service_name="", consumer_name="", stream_use=StreamUse.PER_EVENT
        )
        self._object_registry = ObjectRegistry(kicker_config.redis)

    @property
    def object_registry(self):
        return self._object_registry

    @property
    def event_transport(self):
        return self._event_transport


kicker_runtime = KickerRuntime()
