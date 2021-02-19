from functools import wraps
from typing import Callable

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from nidhoggr.core.response import ErrorResponse
from pydantic import ValidationError
from pydantic.main import BaseModel

from lavender.settings import NIDHOGGR_BEARER_TOKEN


def typed(func: Callable[[BaseModel], BaseModel]) -> Callable[[HttpRequest], BaseModel]:
    @wraps(func)
    def wrapper(request: HttpRequest) -> BaseModel:
        try:
            # noinspection PyUnresolvedReferences
            tpe: BaseModel = func.__annotations__['req']  # by convention
            req: BaseModel = tpe.parse_raw(request.body)
        except ValidationError as e:
            return ErrorResponse(reason=f"Failed to decode payload {request.body}", exception=str(e))
        else:
            return func(req)

    return wrapper


def internal(func: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    @wraps(func)
    def wrapper(request: HttpRequest) -> HttpResponse:
        _, *request_token = request.headers.get("Authorization", "").split("Bearer ")
        if len(request_token) != 1:
            return HttpResponseNotFound()
        if request_token[0] != NIDHOGGR_BEARER_TOKEN:
            return HttpResponseForbidden()
        return func(request)

    return wrapper
