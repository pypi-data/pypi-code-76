from functools import wraps
from typing import Type, Optional as Opt, Callable, get_type_hints, Any

from aiohttp.web_exceptions import HTTPBadRequest
from trafaret import Trafaret

from simio.handler.entities import HandlerRequest, RequestSchema, RequestData, AppRoute
from simio.handler.request_validator import (
    RequestValidator,
    AbstractRequestValidator,
    get_bad_request_exception,
)
from simio.handler.wrapper import wrap_handler
from simio.utils import cast_cap_words_to_lower, is_typing


class Router:
    def __init__(self, prefix: str = ""):
        self._prefix = prefix
        self._routes = []

    @property
    def routes(self):
        yield from self._routes

    def handle(
        self,
        method: str,
        path: str,
        name: Opt[str] = None,  # pylint: disable=unused-argument
        request_validator_cls: Type[AbstractRequestValidator] = RequestValidator,
        on_exception_response: Callable[
            [Any], HTTPBadRequest
        ] = get_bad_request_exception,
    ) -> Callable:
        def decorator(handler: Callable) -> Callable:
            nonlocal name

            if name is None:
                name = cast_cap_words_to_lower(handler.__name__)

            handler_request = _create_handler_request(handler, method, path)
            request_validator = request_validator_cls(
                handler_request, on_exception_response
            )
            handler = wrap_handler(handler, request_validator)

            self._add_route(method=method, path=path, handler=handler, name=name)

            return handler

        return decorator

    def __getattr__(self, method) -> Callable:
        @wraps(self.handle)
        def _handle(*args, **kwargs):
            return self.handle(method, *args, **kwargs)

        return _handle

    def _add_route(self, method: str, path: str, handler: Callable, name: str):
        self._routes.append(
            AppRoute(
                method=method, handler=handler, path=self._prefix + path, name=name
            )
        )


def _create_handler_request(
    handler: Callable, method: str, path: str
) -> HandlerRequest:
    handler_request = HandlerRequest(method=method)
    handler_args = get_type_hints(handler)

    handler_args.pop("return", None)

    for arg_name, type_hint in handler_args.items():
        if not isinstance(type_hint, RequestData):
            continue

        type_hint = type_hint.data_type
        if not is_typing(type_hint) and isinstance(type_hint, Trafaret):
            handler_request.request_schema = RequestSchema(
                trafaret=type_hint, name=arg_name
            )
        elif f"{{{arg_name}}}" in path:
            handler_request.path_args[arg_name] = type_hint
        else:
            handler_request.query_args[arg_name] = type_hint

    return handler_request
