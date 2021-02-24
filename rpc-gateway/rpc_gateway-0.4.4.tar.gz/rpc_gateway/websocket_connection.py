from typing import Optional, Dict, Any, Callable, Awaitable
import asyncio
import pickle
import json
import logging
import websockets
from concurrent import futures
from rpc_gateway import messages, errors, utils

logger = logging.getLogger(__name__)
RequestHandlerType = Callable[['WebsocketConnection', messages.Request], Awaitable[messages.Response]]
CloseHandlerType = Callable[['MessagePump'], Awaitable]
MAX_MESSAGE_ID = 99999
last_message_id = 0


def next_message_id() -> int:
    global last_message_id
    last_message_id += 1
    return last_message_id % MAX_MESSAGE_ID


class WebsocketConnection:
    next_id = 0

    def __init__(self,
                 connection: Optional[websockets.WebSocketCommonProtocol] = None,
                 request_handler: Optional[RequestHandlerType] = None,
                 close_handler: Optional[CloseHandlerType] = None,
                 message_queues: Optional[Dict[int, asyncio.Queue]] = None):
        self.id = WebsocketConnection.next_id
        WebsocketConnection.next_id += 1
        self.logger = logger.getChild(self.__class__.__name__)
        self.connection = connection
        self.request_handler = request_handler
        self.close_handler = close_handler
        self.event_loop = asyncio.get_event_loop()
        self.send_queue = asyncio.Queue()
        self.receive_queues = {} if message_queues is None else message_queues
        self.message_send_task: Optional[asyncio.Task] = None
        self.message_receive_task: Optional[asyncio.Task] = None
        self.running = False

    @property
    def connected(self) -> bool:
        return self.connection.open

    async def start(self, wait=True, connection: Optional[websockets.WebSocketCommonProtocol] = None):
        if connection is not None:
            self.connection = connection

        self.running = True
        self.message_send_task = asyncio.Task(self._message_receive())
        self.message_receive_task = asyncio.Task(self._message_send())

        if wait:
            await self.wait()

    async def wait(self):
        try:
            await self.message_send_task
            await self.message_receive_task
        except futures.CancelledError:
            pass

    async def stop(self):
        self.running = False
        await self.connection.close()
        await self.connection.wait_closed()
        self.message_send_task.cancel()
        self.message_receive_task.cancel()
        try:
            await self.message_receive_task
            await self.message_send_task
        except futures.CancelledError:
            pass

    def send_message_sync(self, message: messages.Message):
        utils.await_sync(self.send_message(message), self.event_loop)

    async def send_message(self, message: messages.Message):
        if self.connection is None:
            raise errors.NotConnectedError('Must be connected to send message: {message}')

        await self.send_queue.put(message)

    def send_request_sync(self, method: str, data: Any = None) -> messages.Response:
        return utils.await_sync(self.send_request(method, data), self.event_loop)

    async def send_request(self, method: str, data: Any = None) -> messages.Response:
        return await self.request(messages.Request(method=method, data=data))

    def send_response_sync(self, id: int, data: Any = None, status: int = messages.Status.SUCCESS):
        utils.await_sync(self.send_response(id, data, status), self.event_loop)

    async def send_response(self, id: int, data: Any = None, status: int = messages.Status.SUCCESS):
        response = messages.Response(id=id, status=status, data=data)
        await self.send_message(response)

    def send_error_response_sync(self, id: int, error: Exception):
        utils.await_sync(self.send_error_response(id, error), self.event_loop)

    async def send_error_response(self, id: int, error: Exception):
        response = messages.Response(id=id, status=messages.Status.ERROR, data=error)
        await self.send_message(response)

    def request_sync(self, request: messages.Request, raise_error=True) -> messages.Response:
        return utils.await_sync(self.request(request, raise_error))

    async def request(self, request: messages.Request, raise_error=True) -> messages.Response:
        request.id = next_message_id()
        queue = self.receive_queues[request.id] = asyncio.Queue()
        await self.send_message(request)

        try:
            response: messages.Response = await queue.get()
            self.receive_queues.pop(request.id)
        except asyncio.TimeoutError:
            self.receive_queues.pop(request.id)
            raise errors.RequestTimeoutError(f'Request timed out while waiting for response: {request}')

        if response.status == messages.Status.ERROR and raise_error:
            raise response.data

        return response

    async def _handle_request(self, request: messages.Request):
        id = request.id
        encoding = request.encoding
        response = await self.request_handler(self, request)
        response.id = id
        response.encoding = encoding
        await self.send_message(response)

    async def _message_send(self):
        while self.running:
            message: messages.Message = await self.send_queue.get()

            try:
                message_bytes = messages.encode(message)
            except (pickle.PickleError, AttributeError):
                message_bytes = messages.Response(id=message.id, status=messages.Status.ERROR, data=errors.SerializationError(f'Cannot serialize response data')).to_pickle()

            self.logger.info(f'[{self.id}] > {message}')
            await self.connection.send(message_bytes)

    async def _message_receive(self):
        try:
            while self.running:
                message_bytes = await self.connection.recv()
                try:
                    message = messages.decode(message_bytes)
                except (pickle.UnpicklingError, TypeError):
                    self.logger.error(f'Invalid message: {message_bytes}')
                    continue

                self.logger.info(f'[{self.id}] < {message}')

                if isinstance(message, messages.Response):  # response
                    if message.id not in self.receive_queues:
                        raise errors.InvalidMessageIdError(f'No request found for response ID: {message.id}')

                    queue = self.receive_queues[message.id]
                    await queue.put(message)

                elif isinstance(message, messages.Request):  # request
                    if self.request_handler is not None:
                        asyncio.create_task(self._handle_request(message))

                else:
                    self.logger.error(f'Invalid message: {message}')

        except websockets.ConnectionClosed as err:
            self.logger.info(f'[{self.id}] Connection closed')

            if isinstance(err, websockets.ConnectionClosedError):
                self.logger.error(err)

            if self.close_handler is not None:
                await self.close_handler(self)