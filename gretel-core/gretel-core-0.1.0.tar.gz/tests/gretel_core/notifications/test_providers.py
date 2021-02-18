from unittest.mock import patch

import pytest

from gretel_core.notifications import DefaultMessage, SlackProvider, ProviderError


class MockResponse:
    status_code = 200
    text = "ok"


def test_slack_provider_success():
    msg = DefaultMessage(
        title="message",
        header={"summary": "the summary"},
        body={"message": "v important"},
        footer={"trace-id": 123}
    )
    slack = SlackProvider("https://hooks.slack.com/services/foo")

    with patch("requests.post") as post:
        post.return_value = MockResponse()
        slack.notify(msg)

    _, args, kwargs = post.mock_calls[0]
    assert "https://hooks.slack.com/services/foo" in args
    payload = kwargs["json"]
    assert "blocks" in payload


def test_slack_provider_bad_http_code():
    msg = DefaultMessage(
        title="message",
        header={"summary": "the summary"},
        body={"message": "v important"},
        footer={"trace-id": 123}
    )
    slack = SlackProvider("https://hooks.slack.com/services/foo")

    with patch("requests.post") as post:
        resp = MockResponse()
        resp.status_code = 400
        post.return_value = resp

        with pytest.raises(ProviderError):
            slack.notify(msg)


def test_slack_provider_non_ok_text():
    msg = DefaultMessage(
        title="message",
        header={"summary": "the summary"},
        body={"message": "v important"},
        footer={"trace-id": 123}
    )
    slack = SlackProvider("https://hooks.slack.com/services/foo")

    with patch("requests.post") as post:
        resp = MockResponse()
        resp.text = "nope"
        post.return_value = resp

        with pytest.raises(ProviderError):
            slack.notify(msg)


def test_slack_bad_url():
    with pytest.raises(ValueError):
        SlackProvider("https://foo.bar")
