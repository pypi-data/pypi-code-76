import os
from functools import wraps
from typing import Callable

from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from pydantic import BaseModel

from lavender.models import Player

access_header = "X-Lavender-Access"
client_header = "X-Lavender-Client"

Decorator = Callable[[HttpRequest], HttpResponse]


def authenticated(func: Callable[[Player, HttpRequest], BaseModel]):
    @wraps(func)
    def wrapper(request: HttpRequest):
        access_token = request.headers.get(access_header)
        client_token = request.headers.get(client_header)
        if not all((access_header, client_header)):
            raise HttpResponseForbidden

        try:
            player: Player = Player.objects.get(token__access=access_token, token__client=client_token)
        except (Player.DoesNotExist, Player.MultipleObjectsReturned):
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
