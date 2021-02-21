import pytest
from uuid import uuid4

from nidhoggr.core.repository import BaseUserRepo
from nidhoggr.errors.auth import MigrationDone, InvalidCredentials, InvalidClientToken
from nidhoggr.errors.common import BadPayload
from nidhoggr.models.auth import Agent, UserInstance, AuthenticationResponse
from .conftest import check_uuid
from ..conftest import cast

nonstring_values = ([1], {2: 3}, None)


def test_empty_credentials(authenticate, user):
    assert cast[BadPayload](authenticate({}))
    assert cast[BadPayload](authenticate({"username": user.email}))
    assert cast[BadPayload](authenticate({"password": user.password}))


@pytest.mark.parametrize(["password"], [(v,) for v in nonstring_values])
@pytest.mark.parametrize(["username"], [(v,) for v in nonstring_values])
def test_nonstring_credentials(authenticate, username, password):
    response = authenticate({
        "username": username,
        "password": password
    })
    assert cast[BadPayload](response)


def test_nonexistent_user(authenticate):
    response = authenticate({
        "username": "unknown@ponyville.eq",
        "password": "anything"
    })
    assert response.status_code == 403
    assert cast[InvalidCredentials](response)


def test_wrong_password(user, authenticate):
    response = authenticate({
        "username": user.email,
        "password": "anything"
    })
    assert response.status_code == 403
    assert cast[InvalidCredentials](response)


@pytest.mark.skip_bl_on(simple_login=True)
def test_migration_done(user, authenticate):
    response = authenticate({
        "username": user.login,
        "password": user.password
    })
    assert response.status_code == 403
    assert cast[MigrationDone](response)


@pytest.mark.skip_bl_on(simple_login=False)
def test_success_simple_login(user, authenticate):
    response = authenticate({
        "username": user.login,
        "password": user.password
    })
    assert response.status_code == 200


def test_success_simple(user, authenticate):
    response = authenticate({
        "username": user.email,
        "password": user.password
    })
    assert response.status_code == 200


def test_access_token_refreshed(users: BaseUserRepo, user, authenticate):
    response = authenticate({
        "username": user.email,
        "password": user.password
    })
    assert response.status_code == 200
    result = cast[AuthenticationResponse](response)
    assert result is not None
    assert result.accessToken != user.access
    fresh = users.get_user(uuid=user.uuid)
    assert fresh.access == result.accessToken


def test_access_token_generated(users: BaseUserRepo, old_user, authenticate):
    response = authenticate({
        "username": old_user.email,
        "password": old_user.password
    })
    assert response.status_code == 200
    result = cast[AuthenticationResponse](response)
    assert result is not None
    check_uuid(result.accessToken)
    fresh = users.get_user(uuid=old_user.uuid)
    assert fresh.access == result.accessToken


def test_client_token_generated(users: BaseUserRepo, new_user, authenticate):
    response = authenticate({
        "username": new_user.email,
        "password": new_user.password,
    })
    assert response.status_code == 200
    result = cast[AuthenticationResponse](response)
    assert result is not None
    check_uuid(result.clientToken)
    fresh = users.get_user(uuid=new_user.uuid)
    assert fresh.client == result.clientToken


def test_client_token_mirrored_back(user, authenticate):
    response = authenticate({
        "username": user.email,
        "password": user.password,
        "clientToken": user.client
    })
    assert response.status_code == 200
    result = cast[AuthenticationResponse](response)
    assert result is not None
    check_uuid(result.clientToken)
    assert user.client == result.clientToken


@pytest.mark.skip_bl_on(strict=True)
def test_client_token_rewritten(users: BaseUserRepo, user, authenticate):
    new_client_token = uuid4()
    response = authenticate({
        "username": user.email,
        "password": user.password,
        "clientToken": new_client_token
    })
    assert response.status_code == 200
    result = cast[AuthenticationResponse](response)
    assert result is not None
    check_uuid(result.clientToken)
    fresh = users.get_user(uuid=user.uuid)
    assert new_client_token == result.clientToken
    assert fresh.client == result.clientToken


@pytest.mark.skip_bl_on(strict=False)
def test_client_token_rejected(user, authenticate):
    new_client_token = uuid4()
    response = authenticate({
        "username": user.email,
        "password": user.password,
        "clientToken": new_client_token
    })
    assert cast[InvalidClientToken](response)


def test_profiles_request(user, authenticate):
    response = authenticate({
        "username": user.email,
        "password": user.password,
        "agent": Agent().dict()
    })
    assert response.status_code == 200
    result = cast[AuthenticationResponse](response)
    assert result is not None
    assert isinstance(result.availableProfiles, list)
    assert len(result.availableProfiles) == 1
    assert result.availableProfiles[0] == result.selectedProfile


def test_user_instance_request(user, authenticate):
    response = authenticate({
        "username": user.email,
        "password": user.password,
        "requestUser": True
    })
    assert response.status_code == 200
    result = cast[AuthenticationResponse](response)
    assert result is not None
    assert isinstance(result.user, UserInstance)
