import operator
from functools import reduce
from typing import Union, Optional

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from lavender.models import Player, Token
from lavender.views.api.decorator import json_response
from nidhoggr.core.repository import BaseUserRepo
from nidhoggr.core.response import StatusResponse, ErrorResponse
from nidhoggr.core.user import UserRequest, User, PasswordRequest

from lavender.decorators import typed, internal


def _user_request_fields(req: UserRequest) -> Optional[Q]:
    filters = []
    if req.login is not None:
        filters.append(Q(username=req.login))
    if req.email is not None:
        filters.append(Q(email=req.email))
    if req.uuid is not None:
        filters.append(Q(token__uuid=req.uuid))
    if req.access is not None:
        filters.append(Q(token__access=req.access))
    if req.client is not None:
        filters.append(Q(token__client=req.client))
    if req.server is not None:
        filters.append(Q(token__server_id=req.server))
    if not filters:
        return None
    return reduce(operator.or_, filters)


@csrf_exempt
@internal
@json_response
@typed
def get(req: UserRequest) -> Union[ErrorResponse, User]:
    filters = _user_request_fields(req)
    if filters is None:
        return ErrorResponse(reason="No valid user filters")
    try:
        player: Player = Player.objects.select_related('token').get(filters)
    except (Player.DoesNotExist, Player.MultipleObjectsReturned):
        return BaseUserRepo.EMPTY_USER

    return User(
        uuid=player.token.uuid,
        login=player.username,
        email=player.email,
        access=player.token.access,
        client=player.token.client,
        server=player.token.server_id,
        properties=[],
    )


@csrf_exempt
@internal
@json_response
@typed
def check_password(req: PasswordRequest) -> Union[ErrorResponse, StatusResponse]:
    try:
        player: Player = Player.objects.get(token__uuid=req.uuid)
    except (Player.DoesNotExist, Player.MultipleObjectsReturned) as e:
        return ErrorResponse(reason=f"No such user with uuid {req.uuid}", exception=str(e))
    status = player.check_password(req.password)
    return StatusResponse(status=status)


@csrf_exempt
@internal
@json_response
@typed
def save(req: User) -> Union[ErrorResponse, User]:
    try:
        token: Token = Token.objects.get(uuid=req.uuid)
    except (Token.DoesNotExist, Token.MultipleObjectsReturned) as e:
        return ErrorResponse(reason=f"No such token for uuid {req.uuid}", exception=str(e))

    # Do not alter any of user's properties (by now)
    token.access = req.access
    token.client = req.client
    token.server_id = req.server
    token.save()
    return req
