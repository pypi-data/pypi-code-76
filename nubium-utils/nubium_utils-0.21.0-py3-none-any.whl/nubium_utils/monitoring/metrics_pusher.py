"""
Class for pushing metrics to Prometheus metrics cache (pushgateway)
"""
import socket
import logging

from prometheus_client import push_to_gateway

LOGGER = logging.getLogger()


class MetricsPusher:
    """
    Pushes metrics to a prometheus pushgateway
    """

    def __init__(self, job, registry, metrics_service_name, metrics_service_port, metrics_pod_port):
        """
        Initializes metrics pusher

        :param job: (str) Unique name of running application
        :param registry: (CollectorRegistry) Registry for all gauges
        :param metrics_service_name: (str) host name of metrics service
        :param metrics_service_port: (sr) port of metrics service
        :param metrics_pod_port: (str) port for metrics cache on individual pod
        """
        self.job = job
        self.registry = registry
        self.metrics_service_name = metrics_service_name
        self.metrics_service_port = metrics_service_port
        self.metrics_pod_port = metrics_pod_port

        self.gateways = None

    def set_gateways(self):
        """
        Queries metrics service for gateway IP addresses

        A single Kubernetes service redirects to multiple IP addresses for
        redundant Prometheus pushgateways.
        :return: None
        """
        socket_info_list = socket.getaddrinfo(
            self.metrics_service_name, self.metrics_service_port)
        self.gateways = {f'{result[-1][0]}:{self.metrics_pod_port}'
                         for result in socket_info_list}
        LOGGER.debug(f'Set gateway addresses: {self.gateways}')

    def push_metrics(self):
        for gateway in self.gateways:
            try:
                push_to_gateway(gateway, job=self.job, registry=self.registry)
            except Exception as error:
                LOGGER.error(f'Failed to push to pushgateway {gateway}\n{error}')