from functools import wraps
from typing import Callable, Any

from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from pydantic import BaseModel

from lavender.models import Player

access_header = "X-Lavender-Access"
client_header = "X-Lavender-Client"

Decorator = Callable[[HttpRequest], HttpResponse]


def authenticated(func: Callable[[Player, HttpRequest], BaseModel]):
    @wraps(func)
    def wrapper(request: HttpRequest):
        access_token = request.headers[access_header]
        client_token = request.headers[client_header]
        if not all((access_header, client_header)):
            raise HttpResponseForbidden

        player: Player = Player.objects.get(token__access=access_token, token__client=client_token)
        if player is None:
            raise HttpResponseForbidden

        response = func(player, request)
        return response

    return wrapper


def json_response(func: Callable[[HttpRequest], BaseModel]) -> Decorator:
    @wraps(func)
    def wrapper(request: HttpRequest):
        result = func(request)
        return HttpResponse(result.json(), status=200, content_type='application/json')

    return wrapper
