"""Console scripts"""
import asyncio
import logging
import sys
import tempfile
import uuid
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Union

import click
import toml


from datastreamcorelib.logging import init_logging
from datastreamcorelib.binpackers import ensure_utf8
from datastreamcorelib.pubsub import PubSubMessage, Subscription
from datastreamcorelib.datamessage import PubSubDataMessage
from datastreamcorelib.imagemessage import PubSubImageMessage
from datastreamservicelib.service import SimpleService


LOGGER = logging.getLogger(__name__)


@dataclass
class Publisher(SimpleService):
    """Publisher service"""

    topic: bytes
    send_count: int = field(default=-1)
    images: bool = field(default=False)

    def reload(self) -> None:
        """Create task for sending messages"""
        super().reload()
        asyncio.get_event_loop().create_task(self.message_sender())

    async def message_sender(self) -> None:
        """Send messages"""
        msgno = 0
        while self.psmgr.default_pub_socket and not self.psmgr.default_pub_socket.closed:
            msgno += 1
            msg: Union[None, PubSubImageMessage, PubSubDataMessage] = None
            if self.images:
                msg = PubSubImageMessage(topic=self.topic)
                msg.imginfo["format"] = "bgr8"
                msg.imginfo["w"] = 1
                msg.imginfo["h"] = 1
                msg.imgdata = bytes((0, 0, 255))
            else:
                msg = PubSubDataMessage(topic=self.topic)
            if not msg:
                raise RuntimeError("We should not reach this ever")
            msg.data["msgno"] = msgno
            LOGGER.debug("Publishing {}".format(msg))
            await self.psmgr.publish_async(msg)
            if self.send_count > 0 and msgno > self.send_count:
                return self.quit()
            await asyncio.sleep(0.1)
        return None


@dataclass
class CollectingSubscriber(SimpleService):
    """Subscriber service that track received messages"""

    topic: bytes
    recv_count: int = field(default=-1)
    messages_by_sub: Dict[uuid.UUID, List[PubSubMessage]] = field(default_factory=dict)
    decoder_class: Any = field(default=PubSubDataMessage)

    def reload(self) -> None:
        """Create subscription"""
        super().reload()
        sub = Subscription(
            self.config["zmq"]["sub_sockets"],
            self.topic,
            self.success_callback,
            decoder_class=self.decoder_class,
            isasync=True,
        )
        self.messages_by_sub[sub.trackingid] = []
        self.psmgr.subscribe_async(sub)

    async def success_callback(self, sub: Subscription, msg: PubSubMessage) -> None:
        """Append the message to the correct list"""
        if sub.trackingid not in self.messages_by_sub:
            self.messages_by_sub[sub.trackingid] = []
        self.messages_by_sub[sub.trackingid].append(msg)
        LOGGER.debug("Got msg {}".format(msg))
        if self.recv_count > 0 and len(self.messages_by_sub[sub.trackingid]) >= self.recv_count:
            self.quit()

    async def teardown(self) -> None:
        """Clean up the messages_by_sub"""
        self.messages_by_sub = {}
        return await super().teardown()


@click.command()
@click.option("-s", "--socket_uri", help="For example ipc:///tmp/publisher.sock", required=True)
@click.option("-t", "--topic", help="The topic to use for sending", required=True)
@click.option("-i", "--images", help="Send images (one red pixel)", is_flag=True)
@click.option("-c", "--count", help="Number of messages to send", type=int, default=-1)
def publisher_cli(socket_uri: str, topic: str, count: int, images: bool) -> None:
    """CLI entrypoint for publisher"""
    init_logging(logging.DEBUG)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug("sys.argv={}".format(sys.argv))
    with tempfile.TemporaryDirectory() as tmpdir:
        configpath = Path(tmpdir) / "config.toml"
        LOGGER.debug("writing file {}".format(configpath))
        with open(configpath, "wt", encoding="utf-8") as fpntr:
            toml.dump({"zmq": {"pub_sockets": [socket_uri]}}, fpntr)
        pub_instance = Publisher(configpath, ensure_utf8(topic), count, images)
        exitcode = asyncio.get_event_loop().run_until_complete(pub_instance.run())
    sys.exit(exitcode)


@click.command()
@click.option("-s", "--socket_uri", help="Must be same the publisher uses", required=True)
@click.option("-t", "--topic", help="The topic to use for receiving, must match topic used in publisher", required=True)
@click.option("-i", "--images", help="Use image decoder", is_flag=True)
@click.option("-c", "--count", help="Number of messages to send", type=int, default=-1)
def subscriber_cli(socket_uri: str, topic: str, count: int, images: bool) -> None:
    """CLI entrypoint for subscriber"""
    init_logging(logging.DEBUG)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug("sys.argv={}".format(sys.argv))
    with tempfile.TemporaryDirectory() as tmpdir:
        configpath = Path(tmpdir) / "config.toml"
        LOGGER.debug("writing file {}".format(configpath))
        with open(configpath, "wt", encoding="utf-8") as fpntr:
            toml.dump({"zmq": {"sub_sockets": [socket_uri]}}, fpntr)
        sub_instance = CollectingSubscriber(configpath, ensure_utf8(topic), count)
        if images:
            sub_instance.decoder_class = PubSubImageMessage
        exitcode = asyncio.get_event_loop().run_until_complete(sub_instance.run())
    sys.exit(exitcode)
