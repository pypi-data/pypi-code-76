from dataclasses import dataclass, field
from typing import Optional as Opt, TypeVar, Type, Callable, Awaitable

from aiohttp import web
from trafaret import Trafaret

T = TypeVar("T")
Handler = Callable[[], Awaitable[web.Response]]


@dataclass
class RequestSchema:
    trafaret: Trafaret
    name: str


@dataclass
class HandlerRequest:
    """
    Describes HTTP method of BaseHandler

    path_args and query_args contains dict where
    keys are names of args and value are type hints
    """

    method: str

    request_schema: Opt[RequestSchema] = None
    path_args: dict = field(default_factory=dict)
    query_args: dict = field(default_factory=dict)


@dataclass
class AppRoute:
    handler: Handler
    method: str
    path: str
    name: str
    handler_request: Opt[HandlerRequest] = None

    def as_route_def(self) -> web.RouteDef:
        return web.route(
            path=self.path, handler=self.handler, name=self.name, method=self.method
        )


@dataclass(frozen=True)
class RequestData:
    data_type: Type[T]

    def __call__(self, *args, **kwargs):
        """ hack for type hinting """
        return self


class _Request:
    def __getitem__(self, data_type: Type[T]) -> Type[T]:
        return RequestData(data_type)


R = _Request()
