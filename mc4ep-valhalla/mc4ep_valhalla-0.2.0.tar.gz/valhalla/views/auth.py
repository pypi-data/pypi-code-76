import os
from random import getrandbits

from flask import request, current_app
from flask_redis import FlaskRedis
from nidhoggr.core.repository import BaseUserRepo
from nidhoggr.core.user import User
from werkzeug.exceptions import BadRequest

from valhalla.decorators import as_json
from valhalla.jwt import generate_auth_token
from valhalla.models import (
    AuthFirstPhaseRequest,
    AuthFirstPhaseResponse,
    AuthSecondPhaseRequest,
    AuthSecondPhaseResponse,
    AuthCookie
)
from valhalla.utils import validate_form, handle_status

SERVER_ID = os.getenv('SERVER_ID')
AUTH_COOKIE_EXPIRE = int(os.getenv('AUTH_COOKIE_EXPIRE'))


@as_json
def handshake() -> AuthFirstPhaseResponse:
    redis: FlaskRedis = current_app.redis

    req = handle_status(validate_form(form=request.form, clazz=AuthFirstPhaseRequest))
    token = getrandbits(32)

    redis.set(req.name, AuthCookie(ip=request.remote_addr, token=token).json(), ex=AUTH_COOKIE_EXPIRE)

    return AuthFirstPhaseResponse(
        offline=False,  # Don't support offline mode
        serverId=SERVER_ID,
        verifyToken=token
    )


@as_json
def response():
    redis: FlaskRedis = current_app.redis
    users: BaseUserRepo = current_app.users

    req = handle_status(validate_form(form=request.form, clazz=AuthSecondPhaseRequest))

    cookie_raw = redis.get(req.name)
    redis.delete(req.name)

    if not cookie_raw:
        raise BadRequest(description='Invalid or expired cookie, try again')

    cookie = AuthCookie.parse_raw(cookie_raw)

    if cookie.ip != request.remote_addr:
        raise BadRequest(description='Unauthenticated network')
    if cookie.token != req.verifyToken:
        raise BadRequest(description='Wrong token')

    user: User = handle_status(users.get_user(login=req.name))

    token = generate_auth_token(user=user)

    return AuthSecondPhaseResponse(accessToken=token)
