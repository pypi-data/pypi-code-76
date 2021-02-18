from dataclasses import dataclass, is_dataclass, fields
import asyncio
import json
import logging
import random
import typing
import copy
import re

from pysignald_async.error import raise_error


@dataclass
class Handler:
    """
    Allows to await for a specific message sent by JSONProtocol.
    This should not be used directly, but rather using
    JSONProtocol.get_future_for(validator).

    validator: a Callable that will receive the response and return True
        if the response is the one it was waiting for
    callback: a Callable that will be called with the response as argument
    """

    validator: typing.Callable
    callback: typing.Callable

    def validate(self, response):
        return self.validator(response)


class JSONProtocol(asyncio.Protocol):
    def __init__(self, on_con_lost: asyncio.Future = None):
        """
        on_con_lost: asyncio.Future: its result will be set to True once
            the connection is lost
        """
        self._buffer = bytearray()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.transport = None

        if on_con_lost is None:
            on_con_lost = asyncio.get_running_loop().create_future()

        self.on_con_lost = on_con_lost
        self.callbacks = {}
        self.specific_handlers = []

    def connection_made(self, transport: asyncio.Transport):
        self.logger.info("Connection established")
        self.transport = transport

    def connection_lost(self, exc: typing.Union[Exception, None]):
        self.logger.info(f"Connection lost: {exc}")
        self.transport = None
        try:
            self.on_con_lost.set_result(True)
        except asyncio.InvalidStateError:
            pass

    def data_received(self, data: bytes):
        """
        Handle data received through the UNIX socket, convert it to a python
        dict and dispatch it to the relevant callback or handler.

        Callbacks can either:
        - wait for a specific payload id, for this you should use the coroutine
          JSONProtocol.get_response
        - wait for a more generic matching payload, for this you should use the
          coroutine JSONProtocol.get_future_for

        In case no callbacks match the payload, it is sent to the method
        JSONProtocol.handle_{payload.type}.
        """
        buffer = self._buffer
        buffer += data
        if not buffer.endswith(b"\n"):
            # print(data)
            return
        # data = self._buffer
        data = buffer
        self._buffer = bytearray()

        for line in data.decode("utf-8").split("\n"):
            if not line:
                continue  # Empty lines are sometimes sent apparently…

            payload = json.loads(line)
            self.logger.debug(
                "Received payload:"
                + "\n"
                + json.dumps(payload, indent=4, sort_keys=True)
            )

            for handler in self.specific_handlers:
                if handler.validate(payload):
                    self.logger.debug(f"Found a specific handler")
                    self.specific_handlers.remove(handler)
                    handler.callback(payload)
                    return

            id_ = payload.get("id")
            if id_ is None:
                type_ = payload.get("type")
                try:
                    handler = getattr(self, f"handle_{type_}")
                except AttributeError:
                    self.logger.info(f"No method to handle {type_}, ignoring")
                    return
                handler(payload)
            else:
                callback = self.callbacks.pop(id_, None)
                if callback is None:
                    self.logger.warning(
                        f"Received payload with id but no callbacks were"
                        "registered for it, ignoring"
                    )
                else:
                    callback(payload)

    def send_request(self, payload: dict, id_=None, callback=None):
        """
        Send a JSON payload to the UNIX socket.

        Arguments:
        payload: dict
        id_: identifier of the request. If not specified, a random string is used.
        callback: a Callable that will be called with the response payload
        """
        if self.transport is None:
            self.logger.warning("No transport, cannot send payload")
            return

        if id_ is None:
            id_ = random_id()
        payload["id"] = id_

        if callback is not None:
            self.callbacks[id_] = callback

        self.logger.debug(
            "Send payload" + "\n" + json.dumps(payload, indent=4, sort_keys=True)
        )
        self.transport.write(json.dumps(payload).encode("utf8") + b"\n")

    def get_future_for(self, validator: typing.Callable) -> asyncio.Future:
        """
        Listens to a specific payload with various criteria. Once they are matched,
        set the result of the Future returned by this function to the payload.

        Criteria are matched with the Handler class.
        """
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        handler = Handler(
            validator=validator,
            callback=lambda res: future.set_result(res),
        )
        # monkey patching Future to have a reference to the handler in case we finally
        # dont want to wait for the future to resolve
        future.handler = handler
        self.specific_handlers.append(handler)
        return future

    async def get_response(self, payload: dict) -> dict:
        """
        Coroutine to await the response to a specific payload.
        Can raise exceptions in case the response is an error.
        """
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.send_request(
            payload=payload, callback=lambda payload: future.set_result(payload)
        )
        response = await future
        raise_error(response)
        return response.get("data", dict())


def random_id(length=20):
    return "".join(
        random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(length)
    )


# Vastly inspired from
# https://www.geeksforgeeks.org/creating-nested-dataclass-objects-in-python/
def nested_dataclass(*args, **kwargs):
    def wrapper(check_class):
        # needed here because of circular imports and problem with type
        # annotations
        import pysignald_async.generated as signald_api

        # passing class to investigate
        check_class = dataclass(check_class, **kwargs)
        o_init = check_class.__init__

        def __init__(self, *args, **kwargs):
            for name, value in kwargs.items():
                # getting field type
                ft = check_class.__annotations__.get(name, None)
                if is_dataclass(ft) and isinstance(value, dict):
                    obj = ft(**value)
                    kwargs[name] = obj
                # Wouldn't be necessary if type annotations as strings in
                # dataclasses were valid…
                elif isinstance(ft, str) and isinstance(value, dict):
                    # Escape - to make it possible to translate payload keys in
                    # dataclass field.
                    new_dict = {}
                    for k, v in value.items():
                        new_dict[k.replace("-", "_")] = v
                    value = new_dict
                    obj = getattr(signald_api, ft)(**value)
                    kwargs[name] = obj
                # Even more tricky, List of dataclass, did not find a better
                # way
                elif str(ft).startswith("typing.List[ForwardRef"):
                    ft = str(ft).split("'")[1]
                    obj = [getattr(signald_api, ft)(**x) for x in value]
                    kwargs[name] = obj

                o_init(self, *args, **kwargs)

        check_class.__init__ = __init__

        return check_class

    return wrapper(args[0]) if args else wrapper


def locals_to_request(d: dict):
    """
    Helper for the generated bindings.
    """
    request = {}
    for k, v in d.items():
        if v is None or k == "self":
            continue
        k = k.replace("-", "_")
        if is_dataclass(v):
            request[k] = asdict_non_none(v)
        else:
            request[k] = v
    return request


def asdict_non_none(obj, *, dict_factory=dict):
    """
    Taken from python standard library, modified to handle our nested dataclasses
    and avoid None values
    """
    if not is_dataclass(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner(obj, dict_factory)


def _asdict_inner(obj, dict_factory):
    """
    Taken from python standard library, modified to handle our nested dataclasses
    """
    if is_dataclass(obj):
        result = []
        for f in fields(obj):
            value = _asdict_inner(getattr(obj, f.name), dict_factory)
            if value is None:
                continue
            result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        return type(obj)(*[_asdict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (_asdict_inner(k, dict_factory), _asdict_inner(v, dict_factory))
            for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


_FIELDS = "__dataclass_fields__"
