# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base.version import Version
from twilio.rest.events.v1.sink import SinkList
from twilio.rest.events.v1.subscription import SubscriptionList


class V1(Version):

    def __init__(self, domain):
        """
        Initialize the V1 version of Events

        :returns: V1 version of Events
        :rtype: twilio.rest.events.v1.V1.V1
        """
        super(V1, self).__init__(domain)
        self.version = 'v1'
        self._sinks = None
        self._subscriptions = None

    @property
    def sinks(self):
        """
        :rtype: twilio.rest.events.v1.sink.SinkList
        """
        if self._sinks is None:
            self._sinks = SinkList(self)
        return self._sinks

    @property
    def subscriptions(self):
        """
        :rtype: twilio.rest.events.v1.subscription.SubscriptionList
        """
        if self._subscriptions is None:
            self._subscriptions = SubscriptionList(self)
        return self._subscriptions

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Events.V1>'
