import pytest

from dkist_processing_common._util.interservice_bus import CatalogFrameMessage
from dkist_processing_common._util.interservice_bus import CatalogObjectMessage
from dkist_processing_common._util.message import publish_messages


def test_publish_messages(mocker):
    mocker.patch("dkist_processing_common._util.message.DurableBlockingProducerWrapper")
    messages = [
        CatalogFrameMessage(objectName="testname", conversationId="12345"),
        CatalogObjectMessage(
            objectType="MOVIE", objectName="testmoviename", conversationId="98765"
        ),
    ]
    publish_messages(messages)


def test_invalid_messages(mocker):
    mocker.patch("dkist_processing_common._util.message.DurableBlockingProducerWrapper")
    with pytest.raises(TypeError):
        CatalogFrameMessage()
    with pytest.raises(TypeError):
        CatalogObjectMessage()
