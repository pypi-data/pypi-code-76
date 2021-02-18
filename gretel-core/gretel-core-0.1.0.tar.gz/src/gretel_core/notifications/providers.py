"""
Handlers for sending messages to downstream providers
"""
from typing import TYPE_CHECKING, Callable
from abc import ABC, abstractmethod
import logging

import requests
from requests.exceptions import ConnectionError

import gretel_core.notifications.slack as slack

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


if TYPE_CHECKING:
    from gretel_core.notifications.messages import BaseMessage
else:
    BaseMessage = None


class ProviderError(Exception):
    """Providers should raise this error, even if from a more concrete
    error that the underlying provider raises. This way there is a consistent
    error to catch and it can be introspected for the more specific provider
    error.
    """


class Provider(ABC):
    """Base provider class. All providers should inherit from
    here and this class should not be used directly.
    """

    @abstractmethod
    def notify(self, msg: BaseMessage, formatter: Callable = None):
        pass


class SlackProvider(Provider):
    """Handler for sending messages to Slack webhooks.

    Args:
        webhook_url: A slack webhook URL
    """

    webhook_url: str

    def __init__(self, webhook_url: str):
        if not webhook_url.startswith("https://hooks.slack.com/services"):
            raise ValueError("webhook_url is not for Slack webhooks")
        self.webhook_url = webhook_url

    def notify(self, msg: BaseMessage, formatter: Callable = slack.from_default):
        """Format a ``BaseMessage`` type into a payload to send to a Slack Webhook.
        By default, a formatter is used for handling a ``DefaultMessage.``

        Args:
            msg:  An subclass instance of a ``BaseMessage``
            formatter: A callable that can take a ``BaseMessage`` subclass instance
                as an argument and return a dict payload that can be sent to a
                Slack Webhook endpoint.  If a custom formatter is desired, its 
                entrypoint can be passed here instead.

        Raises:
            ``ProviderError`` if the request could not be completed.
        """
        payload = formatter(msg)
        try:
            res = requests.post(self.webhook_url, json=payload, timeout=5)
        except ConnectionError as err:
            raise ProviderError("Slack connection error") from err

        if res.status_code != 200:
            raise ProviderError(f"Slack got back non-200 OK: {res.text}")

        if res.text != "ok":
            raise ProviderError(f"Slack got back non-ok response: {res.text}")
