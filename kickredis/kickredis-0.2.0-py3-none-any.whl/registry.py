import asyncio
import logging
import redis
from dataclasses import dataclass
from lightbus.message import EventMessage
from lightbus.transports.redis.event import RedisEventTransport, StreamUse
from astra import models
from kickredis.config import KConfig

log = logging.getLogger("kicker.services")

db = redis.StrictRedis(host="127.0.0.1", decode_responses=True)


event_transport = RedisEventTransport(
    service_name="KickerService",
    consumer_name="KickerConsumer",
    stream_use=StreamUse.PER_EVENT,
)


class Column(models.Model):
    def get_db(self):
        return db

    name = models.CharHash()
    unit = models.CharHash()


class Attribute(models.Model):
    def get_db(self):
        return db

    name = models.CharHash()
    values = models.Set()


class AttributeAbleMixin:
    attributes = models.Set(to=Attribute)

    def attr_set(self, attr_name: str, attr_vals: set):
        pk = self._gen_attr_pk(attr_name)

        attr = Attribute(pk=pk, name=attr_name)

        self.attributes.sadd(attr)

        for v in attr_vals:
            attr.values.sadd(v)

    def attr_get(self, attr_name: str) -> set:
        for attr in self.attributes.smembers():
            if attr.name == attr_name:
                return set(attr.values.smembers())
        return None

    def __getattr__(self, name):
        val = self.attr_get(name)
        if val == None:
            self.__getattribute__(name)
        else:
            return val

    def _gen_attr_pk(self, attr_name):
        # class_name_lowecase = __class__.__name__.lower()
        class_name_lowecase = self.get_class_name()

        return f"{class_name_lowecase}##{self.pk}##{attr_name}"


class Stream(models.Model, AttributeAbleMixin):

    REDIS_STREAM_NAME_PREFIX = "KickerStream"

    @staticmethod
    def get_class_name():
        return "stream"

    def get_db(self):
        return db

    name = models.CharHash()
    description = models.CharHash()
    sensor_type = models.CharHash()
    units = models.CharHash()
    data_type = models.CharHash()
    rate = models.CharHash()
    min = models.IntegerField
    max = models.IntegerField

    async def send_value(self, val):
        event_dict = {self.name: val}
        await event_transport.send_event(
            EventMessage(
                api_name=Stream.REDIS_STREAM_NAME_PREFIX,
                event_name=f"{self.pk}",
                id=f"{self.pk}",
                kwargs=event_dict,
            ),
            options={},
        )

    def consume(self, consumer_name: str):
        return event_transport.consume(
            [(Stream.REDIS_STREAM_NAME_PREFIX, f"{self.pk}")],
            consumer_name,
            error_queue=None,
        )

    async def acknowledge(self, msg):
        await event_transport.acknowledge(msg)


class Device(models.Model, AttributeAbleMixin):
    @staticmethod
    def get_class_name():
        return "device"

    def get_db(self):
        return db

    name = models.CharHash()
    uuid = models.CharHash()
    xbee_address = models.CharHash()
    streams = models.Set(to=Stream)

    def add_stream(self, stream_name: str) -> Stream:
        stream_id = f"{self.pk}##{stream_name}"
        strm = Stream(pk=stream_id, name=stream_name)
        self.streams.sadd(strm)
        return strm

    def find_stream_by_name(self, stream_name):
        for strm in self.streams.smembers():
            if strm.name == stream_name:
                return strm
        return None

    @classmethod
    def find_iter(cls):
        for pk in db.scan_iter(match="astra::device*", _type="HASH"):
            yield cls(pk)


@dataclass
class QuestionHandle:
    id: str


class Question:
    def __init__(self, q_id: str):
        self.id = q_id

    def getHandle(self):
        return QuestionHandle(self.id)

    async def run(self, event_transport):
        i = 0
        kstream = Stream(pk=self.id)
        while True:
            log.info(f"Question[{self.id}]:{i}")
            i += 1
            await kstream.send_value(i)

            await asyncio.sleep(1)


class ObjectRegistry:
    def __init__(self, config: KConfig):
        self.config = config

    def add_device(self, dev_id: str) -> Device:
        dev = Device(pk=dev_id, name="")
        return dev

    def find_device(self, dev_id: str) -> Device:
        dev = Device(pk=dev_id)
        return dev
