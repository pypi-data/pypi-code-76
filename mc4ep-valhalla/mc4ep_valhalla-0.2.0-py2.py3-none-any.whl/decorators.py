from functools import wraps
from typing import Callable

from flask import Response
from pydantic import BaseModel
from werkzeug.exceptions import NotFound, Forbidden

from valhalla.jwt import auth

MIME_TYPE = 'application/json'


def as_json_error(func: Callable):
    @wraps(func)
    def wrapper(*view_args, **view_kwargs) -> Response:
        response: BaseModel = func(*view_args, **view_kwargs)
        return Response(
            mimetype=MIME_TYPE,
            content_type=MIME_TYPE,
            status=500,
            response=response.json(exclude_none=True)
        )
    return wrapper


def as_json(func: Callable):
    @wraps(func)
    def wrapper(*view_args, **view_kwargs) -> Response:
        response: BaseModel = func(*view_args, **view_kwargs)
        return Response(
            mimetype=MIME_TYPE,
            content_type=MIME_TYPE,
            response=response.json(exclude_none=True)
        )
    return wrapper


def protected(func: Callable):
    @wraps(func)
    def wrapper(*view_args, **view_kwargs) -> Response:
        auth.login_required(lambda: None)()
        current_user = auth.current_user()
        if current_user is None:
            raise NotFound(description=f"There are no such user")
        if current_user.uuid != view_kwargs['uuid']:  # By convention
            raise Forbidden(description=f"Cannot change another user's textures")
        return func(*view_args, **view_kwargs)
    return wrapper
