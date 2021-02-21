from typing import Union
from uuid import uuid4

from nidhoggr.core.config import BLConfig
from nidhoggr.core.repository import BaseUserRepo
from nidhoggr.core.user import User

from nidhoggr.errors.auth import MigrationDone, InvalidCredentials, InvalidAccessToken, InvalidClientToken
from nidhoggr.errors.common import YggdrasilError, BadRequest
from nidhoggr.models import auth
from nidhoggr.utils.decorator import typed
from nidhoggr.utils.repository import handle_status


@typed
def authenticate(
    req: auth.AuthenticationRequest,
    users: BaseUserRepo,
    config: BLConfig
) -> Union[auth.AuthenticationResponse, YggdrasilError]:
    user: User = handle_status(users.get_user(email=req.username, login=req.username))

    if user.synthetic:
        return InvalidCredentials

    password_check = handle_status(users.check_password(clean=req.password, uuid=user.uuid))
    if not password_check.status:
        return InvalidCredentials

    if not config.simple_login and req.username == user.login:
        return MigrationDone

    if (config.strict and (user.client is None)) or (not config.strict):
        client_token = req.clientToken or uuid4()
        user = user.copy(update=dict(client=client_token))
    elif config.strict and req.clientToken is not None and user.client != req.clientToken:
        return InvalidClientToken

    user = user.copy(update=dict(access=uuid4()))

    if req.agent is not None:
        profile = auth.Profile(id=user.uuid, name=user.login)
        selected_profile, available_profiles = profile, [profile]
    else:
        selected_profile = available_profiles = None

    if req.requestUser:
        user_instance = auth.UserInstance(id=user.uuid, properties=user.properties)
    else:
        user_instance = None

    handle_status(users.save_user(user=user))

    return auth.AuthenticationResponse(
        accessToken=user.access,
        clientToken=user.client,
        availableProfiles=available_profiles,
        selectedProfile=selected_profile,
        user=user_instance,
    )


@typed
def refresh(req: auth.RefreshRequest, users: BaseUserRepo) -> Union[auth.RefreshResponse, YggdrasilError]:
    user: User = handle_status(users.get_user(client=req.clientToken))

    if user.synthetic:
        return BadRequest

    user = user.copy(update=dict(access=uuid4()))
    selected_profile = auth.Profile(id=user.uuid, name=user.login)

    if req.requestUser:
        user_instance = auth.UserInstance(id=user.uuid, properties=user.properties)
    else:
        user_instance = None

    handle_status(users.save_user(user=user))

    return auth.RefreshResponse(
        accessToken=user.access,
        clientToken=user.client,
        selectedProfile=selected_profile,
        user=user_instance,
    )


@typed
def validate(req: auth.ValidateRequest, users: BaseUserRepo) -> Union[auth.EmptyResponse, YggdrasilError]:
    user: User = handle_status(users.get_user(access=req.accessToken))

    if user.synthetic:
        return InvalidAccessToken

    if req.clientToken is not None and req.clientToken != user.client:
        return InvalidClientToken

    return auth.NoContent


@typed
def invalidate(req: auth.InvalidateRequest, users: BaseUserRepo) -> Union[auth.EmptyResponse, YggdrasilError]:
    user: User = handle_status(users.get_user(access=req.accessToken))

    if user.synthetic:
        return InvalidAccessToken

    if req.clientToken != user.client:
        return InvalidClientToken

    user = user.copy(update=dict(access=None))

    handle_status(users.save_user(user=user))

    return auth.NoContent


@typed
def signout(req: auth.SignOutRequest, users: BaseUserRepo) -> Union[auth.EmptyResponse, YggdrasilError]:
    user: User = handle_status(users.get_user(email=req.username))

    if user.synthetic:
        return InvalidCredentials

    password_check = handle_status(users.check_password(clean=req.password, uuid=user.uuid))
    if not password_check.status:
        return InvalidCredentials

    user = user.copy(update=dict(access=None))

    handle_status(users.save_user(user=user))

    return auth.NoContent


__all__ = {"authenticate", "refresh", "validate", "invalidate", "signout"}
