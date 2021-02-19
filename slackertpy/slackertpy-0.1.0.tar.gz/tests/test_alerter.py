import pytest
from unittest.mock import patch

from slackertpy import Alerter, Level


@pytest.fixture
def alerter():
    alerter = Alerter('mock_webhook_url')
    yield alerter


def test_set_level(alerter):
    alerter.set_level(Level.ERROR)
    assert alerter._level == Level.ERROR


def test_send_info_alert(alerter):
    message = {'text': 'simple message'}
    with patch('requests.post') as mock_requests_post:
        alerter.info(message)
        mock_requests_post.assert_called_once()


def test_send_info_alert_level_is_error(alerter):
    alerter.set_level(Level.ERROR)
    message = {'text': 'simple message'}
    with patch('requests.post') as mock_requests_post:
        alerter.info(message)
        mock_requests_post.assert_not_called()
