import pytest

from dkist_processing_common._util.interservice_bus import CatalogFrameMessage
from dkist_processing_common._util.interservice_bus import CatalogObjectMessage
from dkist_processing_common._util.message import publish_messages


def test_publish_messages(mocker):
    mocker.patch("dkist_processing_common._util.message.DurableBlockingProducerWrapper")
    messages = [CatalogFrameMessage(), CatalogObjectMessage(objectType="MOVIE")]
    publish_messages(messages)


def test_invalid_publish_messages(mocker):
    mocker.patch("dkist_processing_common._util.message.DurableBlockingProducerWrapper")
    messages = ["a"]
    with pytest.raises(AttributeError):
        publish_messages(messages)
