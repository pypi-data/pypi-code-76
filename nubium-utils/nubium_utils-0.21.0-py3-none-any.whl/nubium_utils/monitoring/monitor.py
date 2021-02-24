"""
Container for standardized application monitoring gauges
"""
from prometheus_client import Gauge, CollectorRegistry


class Monitor:
    """
    Coordinates Prometheus monitoring for a Kafka client application

    Creates default gauges, and simplifies updates to them
    """

    def __init__(self, job: str, app: str, registry: CollectorRegistry):
        """
        Initializes monitor

        :param job: (str) Unique name of individual application instance
        :param app: (str) Common app name for grouping metrics
        :param registry: (CollectorRegistry) registry for prometheus metrics
        """
        self.job = job
        self.app = app
        self.registry = registry

        self.messages_consumed = Gauge('messages_consumed', 'Messages processed since application start', labelnames=['app', 'job'], registry=self.registry)
        self.messages_produced = Gauge('messages_produced', 'Messages successfully produced since application start', labelnames=['app', 'job'], registry=self.registry)
        self.message_errors = Gauge('message_errors', 'Exceptions caught when processing messages', labelnames=['app', 'job'], registry=self.registry)
