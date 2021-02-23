import json
from abc import ABC, abstractmethod
from typing import Callable, Any, Dict

from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_request import Request
from trafaret import DataError, Trafaret
from typingplus import cast

from simio.handler.entities import HandlerRequest


def get_bad_request_exception(message: Any) -> HTTPBadRequest:
    """
    :param message: text of your exception
    :return: returns HTTPBadRequest exception with json:
            {"error": message}
    """
    body = {"error": message}
    return HTTPBadRequest(reason="Bad Request", body=json.dumps(body).encode())


class AbstractRequestValidator(ABC):
    """Interface for request validators"""

    def __init__(
        self,
        handler_method: HandlerRequest,
        on_exception_response: Callable[[Any], HTTPBadRequest],
    ):
        self._handler_method = handler_method
        self._on_exception_response = on_exception_response

    @abstractmethod
    async def validate(self, request: Request) -> Dict[str, Any]:
        """Validates request and returns kwargs that will be passed to handler"""
        ...


class RequestValidator(AbstractRequestValidator):
    async def validate(self, request: Request) -> Dict[str, Any]:
        kwargs = {}

        for arg_name, type_hint in self._handler_method.path_args.items():
            value = self._cast_type(request.match_info.get(arg_name), type_hint)

            if value is not None:
                kwargs[arg_name] = value

        for arg_name, type_hint in self._handler_method.query_args.items():
            value = self._cast_type(request.query.get(arg_name), type_hint)

            if value is not None:
                kwargs[arg_name] = value

        if self._handler_method.request_schema is not None:
            value = self._cast_type(
                await request.json(), self._handler_method.request_schema.trafaret
            )
            kwargs[self._handler_method.request_schema.name] = value

        return kwargs

    def _cast_type(self, value, type_hint):
        """
        Casting request data
        """
        try:
            if isinstance(type_hint, Trafaret):
                return type_hint.check(value)
            return cast(type_hint, value)
        except DataError as e:
            raise self._on_exception_response(e.as_dict())
        except (ValueError, TypeError) as e:
            raise self._on_exception_response(str(e))
