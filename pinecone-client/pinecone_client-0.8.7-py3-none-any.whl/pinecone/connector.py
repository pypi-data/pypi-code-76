#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable, Callable, Iterator, Tuple, Optional, NamedTuple
import numpy as np

from pinecone.protos import core_pb2
from pinecone.utils import load_numpy
from .api_controller import ControllerAPI
from .api_router import RouterAPI
from .constants import Config
from .grpc import GRPCClient

__all__ = ["connect", "Connection", "Cursor", "IndexResult", "DeleteResult", "QueryResult", "InfoResult", "FetchResult"]


class IndexResult(NamedTuple):
    """Result of an index request."""

    id: str


class DeleteResult(NamedTuple):
    """Result of a delete request."""

    id: str


class QueryResult(NamedTuple):
    """Result of a query request."""

    ids: Iterable[str]
    scores: Iterable[float]
    data: np.ndarray = None


class InfoResult(NamedTuple):
    """Result of an info request"""

    index_size: str


class FetchResult(NamedTuple):
    """Result of a fetch request"""

    id: str
    vector: np.ndarray


class CursorConfig(NamedTuple):
    """Cursor configurations."""

    grpc_client: GRPCClient
    create_request_fn: Callable[[Iterable], Iterator["core_pb2.Request"]]
    parse_response_fn: Optional[Callable[["core_pb2.Response"], Iterable]] = None


class Cursor:
    def __init__(
        self,
        config: CursorConfig,
        items: Iterable[np.ndarray],
        batch_size: int = 100,
    ):
        """A cursor batch-processes requests sent to a service.

        :param config: cursor configurations
        :type config: :class:`CursorConfig`
        :param items: Items to process
        :type items: Iterable[np.ndarray]
        :param batch_size: the number of items to batch-process, defaults to 100
        :type batch_size: int, optional
        """
        self.batch_size = batch_size or 100
        self._item_iterator = iter(items)
        self._client = config.grpc_client
        self._create_reqeust_fn = config.create_request_fn
        self._parse_response_fn = config.parse_response_fn or self.identity

    def take(self, size: int):
        """Processes a given number of items and returns the results.

        :param size: the number of items to process
        """
        result = list(self._fetch_unbuffered(size=size))
        return result or None

    def collect(self):
        """Processes all of the items and returns the results."""
        return list(self._fetch_unbuffered())

    def stream(self):
        """Processes all of the items, returns the results one batch at a time."""
        return self._fetch_unbuffered()

    def __iter__(self):
        raise RuntimeError(
            "To iterate through the results, "
            "consider using one of the followoing methods: `take()`, `collect()`, `stream()`."
        )

    @classmethod
    def identity(cls, entity):
        """An identity function."""
        return entity

    def _fetch_unbuffered(self, size: int = None) -> Iterator:
        """Creates a generator to fetch results.

        :param size: how many items to fetch.
        """
        request_generator = self._generate_requests(size)
        for response in self._client.stream_requests(request_generator):
            if response.status.code == core_pb2.Status.StatusCode.Value("ERROR"):
                exception = bool(response.status.details) and response.status.details[0].exception
                error_msg = exception or response.status.description or "Unknown error when fetching results."
                raise RuntimeError(error_msg)

            for elem in self._parse_response_fn(response):
                yield elem

    def _generate_requests(self, size: int = None) -> Iterator["core_pb2.Request"]:
        """Generates protobuf requests.

        This method consumes the item iterator in batches,
        then creates requests that each wraps the batch of items.

        :param size: how many items to consume. If `None`, th method exhausts the item iterator.
        """
        batch = []
        for ii, item in enumerate(self._item_iterator):
            batch.append(item)
            if len(batch) >= self.batch_size:
                yield self._create_reqeust_fn(batch)
                batch = []
            if not size:
                # consume everything
                continue
            elif ii >= size - 1:
                break
        if batch:
            yield self._create_reqeust_fn(batch)


class Connection:
    """A connection manages communication with a service.

    You can only interact with a service (e.g. upsert, query)
    after a connection to the service has been established.

    Namespaces partition the items in an index. When you read from or write to a namespace in an index, you will
    only access items in that particular namespace.
    For instance, two namespaces can contain the items with the same ids but different values.
    Use namespaces when you want to use the same preprocessors and postprocessors for separate datasets.
    For example, if you are building a movie recommender system, then you could use namespaces to
    separate the recommendations by genre.
    """

    def __init__(self, host: str, port: int, api_key: str = None, service_name: str = None, timeout: int = 0,
                 response_timeout: int = 20, traceroute: bool = False):
        """
        :param host: service host
        :type host: str
        :param port: service port
        :type port: int
        :param api_key: user API key, defaults to None
        :type api_key: str, optional
        :param service_name: name of the service, defaults to None
        :type service_name: str, optional
        :param timeout: defaults to 0. Timeout to retry connection if gRPC is unavailable. 0 is no retry.
        :type timeout: int, optional
        :param response_timeout: defaults to 20 seconds. Fail if gateway doesn't receive response within timeout.
        :type response_timeout: int, optional
        :param traceroute: Whether to send receipts back to the gateway from each stage of the graph
        :type traceroute: bool, optional
        """

        self.host = host
        self.port = port
        self.api_key = api_key
        self.service_name = service_name
        self.grpc = GRPCClient(host=host, port=port, api_key=api_key, service_name=service_name, conn_timeout=timeout,
                               timeout=response_timeout, traceroute=traceroute)

    def upsert(self, items: Iterable[Tuple[str, np.ndarray]], namespace: str = None, batch_size: int = None) -> Cursor:
        """Inserts or updates items.

        Insert an item into the index, or update by item id if the item's id already exists.

        :param items: tuples of the form (id, numpy.ndarray). Id's length is limited to 64 characters.
        :type items: Iterable[Tuple[str, np.ndarray]]
        :param namespace: a partition in an index. Use default namespace when not specified.
        :type namespace: str, optional
        :param batch_size: overrides default batch size
        :type batch_size: int, optional
        :return: :class:`Cursor`
        """

        def _create_index_request(item_batch: Iterable[Tuple[str, np.ndarray]]) -> "core_pb2.Request":
            """Creates an index request using all of the items."""
            path = "write"
            ids_buffer, vectors_buffer = list(zip(*item_batch))
            ids_buffer = list(map(str, ids_buffer))
            return self.grpc.get_index_request(ids=ids_buffer, data=vectors_buffer, namespace=namespace, path=path)

        def _parse_index_response(response):
            return [IndexResult(id=_id) for _id in response.index.ids]

        cursor_config = CursorConfig(
            grpc_client=self.grpc, create_request_fn=_create_index_request, parse_response_fn=_parse_index_response
        )
        return Cursor(config=cursor_config, items=items, batch_size=batch_size)

    def delete(self, ids: Iterable[str], namespace: str = None, batch_size: int = None) -> Cursor:
        """Deletes items by their ids.

        :param ids: ids of items
        :type ids: Iterable[str]
        :param namespace: a partition in an index. Use default namespace when not specified.
        :type namespace: str, optional
        :param batch_size: overrides default batch size
        :type batch_size: int, optional
        :return: :class:`Cursor`
        """

        def _create_delete_request(id_batch: Iterable[str]) -> "core_pb2.Request":
            """Generates a delete request."""
            path = "write"
            return self.grpc.get_delete_request(ids=id_batch, namespace=namespace, path=path)

        def _parse_delete_response(response):
            return [DeleteResult(id=_id) for _id in response.delete.ids]

        cursor_config = CursorConfig(
            grpc_client=self.grpc, create_request_fn=_create_delete_request, parse_response_fn=_parse_delete_response
        )
        return Cursor(config=cursor_config, items=ids, batch_size=batch_size)

    def fetch(self, ids: Iterable[str], namespace: str = None, batch_size: int = None) -> Cursor:
        """Fetches items by their ids.

        :param ids: ids of items
        :type ids: Iterable[str]
        :param namespace: a partition in an index. Use default namespace when not specified.
        :type namespace: str, optional
        :param batch_size: overrides default batch size
        :type batch_size: int, optional
        :return: :class:`Cursor`
        """

        def _create_fetch_request(id_batch: Iterable[str]) -> Iterator["core_pb2.Request"]:
            """Generates a delete request."""
            path = "read"
            return self.grpc.get_fetch_request(ids=id_batch, namespace=namespace, path=path)

        def _parse_fetch_response(response):
            return [
                FetchResult(id=_id, vector=load_numpy(vector))
                for _id, vector in zip(response.fetch.ids, response.fetch.vectors)
            ]

        cursor_config = CursorConfig(
            grpc_client=self.grpc, create_request_fn=_create_fetch_request, parse_response_fn=_parse_fetch_response
        )
        return Cursor(config=cursor_config, items=ids, batch_size=batch_size)

    def query(
        self,
        queries: Iterable[np.ndarray],
        namespace: str = None,
        top_k: int = 10,
        batch_size: int = None,
        include_data: bool = False,
    ) -> Cursor:
        """Sends queries to the index and returns the top results ordered by their scores.

        :param queries: queries
        :type queries: Iterable[np.ndarray]
        :param namespace: a partition in an index. Use default namespace when not specified.
        :type namespace: str, optional
        :param top_k: defaults to 10, the number of top query results to return for each query,
            ordered by their scores
        :type top_k: int, optional
        :param batch_size: overrides default batch size
        :type batch_size: int, optional
        :param include_data: whether to return data associated with the query results, defaults to False
        :type include_data: bool, optional
        :return: :class:`Cursor`
        """

        def _create_query_request(query_batch: Iterable[np.ndarray]) -> "core_pb2.Request":
            """Generates a query request."""
            path = "read"
            return self.grpc.get_query_request(
                data=query_batch, top_k=top_k, include_data=include_data, namespace=namespace, path=path
            )

        def _parse_query_response(response):
            """Parses a query response"""
            return [
                QueryResult(
                    ids=matches.ids,
                    scores=matches.scores,
                    data=load_numpy(matches.data) if response.query.include_data else None,
                )
                for matches in response.query.matches
            ]

        cursor_config = CursorConfig(
            grpc_client=self.grpc, create_request_fn=_create_query_request, parse_response_fn=_parse_query_response
        )
        return Cursor(config=cursor_config, items=queries, batch_size=batch_size)

    def info(self, namespace: str = None) -> InfoResult:
        """Returns information of the index."""

        def _create_info_request(*args):
            path = "write"
            return self.grpc.get_info_request(namespace=namespace, path=path)

        def _parse_info_response(response):
            return [InfoResult(index_size=response.info.index_size)]

        cursor_config = CursorConfig(
            grpc_client=self.grpc, create_request_fn=_create_info_request, parse_response_fn=_parse_info_response
        )
        result = Cursor(config=cursor_config, items=[1]).take(1)
        return result[0] if result else None

    def close(self):
        """Closes the connection."""

        self.grpc.channel.close()

    def _set_secure(self, is_secure: bool):
        """Changes whether the grpc client is secure or not."""

        self.grpc.secure = is_secure


def connect(service_name: str = None, router_name: str = None, timeout: int = 0,
            response_timeout: int = 20, traceroute: bool = False) -> Connection:
    """Connects to a live service/router and returns an instance of :class:`Connection`.

    :param service_name: name of a service.
    :param router_name: name of a router.
    :type service_name: str
    :type router_name: str
    :param timeout: gRPC connection timeout, defaults to 0
    :type timeout: int, optional
    :param timeout: defaults to 0. Timeout to retry connection if gRPC is unavailable. 0 is no retry.
    :type timeout: int, optional
    :param response_timeout: defaults to 20 seconds. Fail if gateway doesn't receive response within timeout.
    :type response_timeout: int, optional
    :param traceroute: Whether to send receipts back to the gateway from each stage of the graph
    :type traceroute: bool, optional
    :return: :class:`Connection`
    """
    dest_name = router_name or service_name
    if not dest_name:
        raise ValueError("Must supply service_name or router_name for connect()")
    api_cls = RouterAPI if router_name else ControllerAPI
    api = api_cls(host=Config.CONTROLLER_HOST, api_key=Config.API_KEY)
    status = api.get_status(dest_name)
    if not status.get("ready"):
        raise ConnectionError

    host = status.get("host") or Config.CONTROLLER_HOST.split("://")[1].split(":")[0]
    port = status.get("port")
    return Connection(host=host, port=port, api_key=Config.API_KEY, service_name=dest_name,
                      timeout=timeout, response_timeout=response_timeout, traceroute=traceroute)
