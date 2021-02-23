#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import List, NamedTuple
import time

from loguru import logger

from .api_controller import ControllerAPI
from .constants import Config
from .graph import Graph

__all__ = ["describe", "deploy", "stop", "ls", "ServiceMeta"]

DEFAULT_TIMEOUT = 60  # seconds


class ServiceMeta(NamedTuple):
    """Metadata of a service."""

    name: str
    graph: Graph
    status: dict


def _get_controller_api():
    return ControllerAPI(host=Config.CONTROLLER_HOST, api_key=Config.API_KEY)


def describe(service_name: str) -> ServiceMeta:
    """Returns the metadata of a service.

    :param service_name: name of the service
    :type service_name: str
    :return: :class:`ServiceMeta`
    """
    api = _get_controller_api()
    service_json = api.get_service(service_name)
    graph = Graph.from_json(service_json) if service_json else None
    return ServiceMeta(name=graph.name, graph=graph, status=api.get_status(service_name) or {})


def deploy(service_name: str, graph: Graph, **kwargs):
    """Create a new Pinecone service from the graph.

    :param service_name: name of the service
    :type service_name: str
    :param graph: the graphical representation fo the service
    :type graph: :class:`pinecone.graph.Graph`
    """
    timeout = kwargs.get("timeout") or DEFAULT_TIMEOUT

    graph.validate()

    # copy graph
    graph_ = Graph.from_json(graph.to_json())
    graph_.name = service_name

    api = _get_controller_api()

    if service_name in api.list_services():
        raise RuntimeError("Service {} already exists.".format(service_name))
    else:
        response = api.deploy(graph_.to_json())

    # Wait for service to deploy
    if timeout > 0:
        start_time = time.perf_counter()
        while True:
            if time.perf_counter() - start_time > timeout:
                raise RuntimeError("Time out when waiting for the service to deploy.")
            status = api.get_status(service_name)
            logger.info("waiting on deployment of: {}".format(status.get("waiting")))
            if status.get("ready"):
                break
            time.sleep(5)

    return response


def stop(service_name: str, **kwargs):
    """Stops a service.

    :param service_name: name of the service
    :type service_name: str
    """
    timeout = kwargs.get("timeout") or DEFAULT_TIMEOUT

    api = _get_controller_api()
    response = api.stop(service_name)

    # Wait for service to stop
    if timeout > 0:
        start_time = time.perf_counter()
        while True:
            if time.perf_counter() - start_time > timeout:
                raise RuntimeError("Time out when waiting for the service to stop.")
            if service_name not in api.list_services():
                break
            time.sleep(5)

    return response


def ls() -> List[str]:
    """Returns all services names."""
    api = _get_controller_api()
    return api.list_services()
