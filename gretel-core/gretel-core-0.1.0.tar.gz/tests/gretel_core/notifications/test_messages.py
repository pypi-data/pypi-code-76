from gretel_core.notifications import DefaultMessage, MessageError


def test_message_error():
    try:
        DefaultMessage()
    except MessageError:
        pass


def test_to_dict():
    msg = DefaultMessage(
        title="le title"
    )
    check = msg.to_dict()
    assert check["title"] == "le title"
    assert check["level"] == "info"
    assert len(check["ts"].split("T")[0].split("-")) == 3
