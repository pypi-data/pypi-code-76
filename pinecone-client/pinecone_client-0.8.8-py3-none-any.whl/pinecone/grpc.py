#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable, List, Union
import grpc, grpc._channel
import uuid
import atexit
import numpy as np

from pinecone import utils
from pinecone.utils.constants import MAX_MSG_SIZE
from pinecone.constants import CLIENT_VERSION
from pinecone.protos import core_pb2_grpc, core_pb2

__all__ = ["GRPCClient"]


class GRPCClient:
    """Client for gRPC."""

    def __init__(
        self,
        host: str = None,
        port: int = None,
        api_key: str = None,
        secure: bool = True,
        service_name: str = None,
        timeout: int = 2,
        conn_timeout: int = 1,
        traceroute: bool = False,
        reuse_channel: bool = True
    ):
        self.host = host
        self.port = port
        self.metadata = (("api-key", api_key), ("service-name", service_name))
        self.secure = secure
        self.timeout = timeout
        self.traceroute = traceroute
        self.conn_timeout = conn_timeout
        self.reuse_channel = reuse_channel
        self._channel = None
        atexit.register(_clean_up_client, client=self)

    @property
    def channel(self):
        """Creates GRPC channel."""
        def _gen():
            target = "{}:{}".format(self.host, self.port)
            options = (("grpc.max_send_message_length", MAX_MSG_SIZE),
                       ("grpc.max_receive_message_length", MAX_MSG_SIZE),)
            if not self.secure:
                return grpc.insecure_channel(target, options=options)
            tls = grpc.ssl_channel_credentials()
            return grpc.secure_channel(target, tls, options=(("grpc.ssl_target_name_override", self.host),) + options)
        if self.reuse_channel and self._channel:
            return self._channel
        self._channel = _gen()
        return self._channel

    def get_index_request(
        self,
        ids: List[str] = None,
        data: Union[np.ndarray, List] = None,
        path: str = None,
        namespace: str = None,
    ) -> "core_pb2.Request":
        """Returns an upsert request."""
        req = core_pb2.IndexRequest()
        if ids is not None:
            req.ids[:] = [str(ee) for ee in ids]
        if data is not None:
            req.data.CopyFrom(utils.dump_numpy(_to_ndarray(data)))
        return core_pb2.Request(
            request_id=_generate_request_id(),
            version=CLIENT_VERSION,
            index=req,
            path=path,
            namespace=namespace,
            timeout=self.timeout,
            traceroute=self.traceroute
        )

    def get_delete_request(
        self,
        ids: Iterable[str],
        path: str = None,
        namespace: str = None,
    ) -> "core_pb2.Request":
        """Returns a delete request."""
        req = core_pb2.DeleteRequest(ids=ids)
        return core_pb2.Request(
            request_id=_generate_request_id(),
            version=CLIENT_VERSION,
            delete=req,
            path=path,
            namespace=namespace,
            timeout=self.timeout,
            traceroute=self.traceroute
        )

    def get_fetch_request(
        self,
        ids: Iterable[str],
        path: str = None,
        namespace: str = None,
    ) -> "core_pb2.Request":
        """Returns a fetch request."""
        req = core_pb2.FetchRequest(ids=ids)
        return core_pb2.Request(
            request_id=_generate_request_id(),
            version=CLIENT_VERSION,
            fetch=req,
            path=path,
            namespace=namespace,
            timeout=self.timeout,
            traceroute=self.traceroute
        )

    def get_query_request(
        self,
        top_k: int = None,
        include_data: bool = None,
        data: Union[np.ndarray, List] = None,
        matches: List[dict] = None,
        path: str = None,
        namespace: str = None,
    ) -> "core_pb2.Request":
        """Returns a query request."""
        req = core_pb2.QueryRequest()
        if top_k is not None:
            req.top_k = top_k
        if include_data is not None:
            req.include_data = include_data
        if data is not None:
            req.data.CopyFrom(utils.dump_numpy(_to_ndarray(data)))
        if matches is not None:
            req.matches.extend([
                core_pb2.ScoredResults(
                    ids=mat.get("ids"),
                    scores=mat.get("scores"),
                    data=utils.dump_numpy(np.array(mat["data"])) if mat.get("data") else None,
                )
                for mat in matches
            ])
        return core_pb2.Request(
            request_id=_generate_request_id(),
            version=CLIENT_VERSION,
            query=req,
            path=path,
            namespace=namespace,
            timeout=self.timeout,
            traceroute=self.traceroute
        )

    def get_info_request(
        self,
        path: str = None,
        namespace: str = None,
    ) -> "core_pb2.Request":
        """Returns an info request"""
        return core_pb2.Request(
            request_id=_generate_request_id(),
            version=CLIENT_VERSION,
            info=core_pb2.InfoRequest(),
            path=path,
            namespace=namespace,
            timeout=self.timeout,
            traceroute=self.traceroute
        )

    def grpc_server_on(self) -> bool:
        try:
            grpc.channel_ready_future(self.channel).result(timeout=self.conn_timeout)
            return True
        except grpc.FutureTimeoutError:
            return False

    def stream_requests(self, request_stream):
        """Creates sub to send proptobuf requests."""
        stub = core_pb2_grpc.RPCClientStub(self.channel)
        if self.conn_timeout > 0 and not self.grpc_server_on():
            raise ConnectionError("Failed to connect to gRPC host {}:{}".format(self.host, self.port))
        exception = None
        try:
            for response in stub.Call(request_stream, metadata=self.metadata):
                yield response
        except grpc._channel._MultiThreadedRendezvous as e:
            exception = e
        if exception:
            raise ConnectionError("Failed to connect to gRPC remote {}:{}. Status = {}. Details = {}. Debug = {}".format(
                self.host, self.port, exception._state.code, exception.details(), exception.debug_error_string()))

    def send_request(self, request):
        stub = core_pb2_grpc.RPCClientStub(self.channel)
        if self.conn_timeout > 0 and not self.grpc_server_on():
            raise ConnectionError("Failed to connect to gRPC host {}:{}".format(self.host, self.port))
        try:
            return stub.CallUnary(request, metadata=self.metadata)
        except grpc._channel._MultiThreadedRendezvous as e:
            exception = e
        raise ConnectionError("Failed to connect to gRPC remote {}:{}. Status = {}. Details = {}. Debug = {}".format(
                self.host, self.port, exception._state.code, exception.details(), exception.debug_error_string()))


def _to_ndarray(arr: Iterable) -> np.ndarray:
    """Convert an array to a numpy array by making best guesses."""
    if isinstance(arr, np.ndarray):
        return arr
    else:
        return np.asarray(arr)


def _generate_request_id() -> int:
    return uuid.uuid4().int & (1 << 64) - 1


def _clean_up_client(client: GRPCClient):
    """Cleans up client resources"""
    try:
        client.channel.close()
    except TypeError:
        pass
