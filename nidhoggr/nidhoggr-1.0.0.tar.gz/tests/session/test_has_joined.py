from typing import Optional
from uuid import uuid4

import pytest

from nidhoggr.errors.auth import InvalidProfile
from nidhoggr.errors.common import BadPayload
from nidhoggr.errors.session import InvalidServer
from nidhoggr.models.session import JoinedResponse
from ..conftest import cast, generate_server_id


optional_ip = pytest.mark.parametrize(
    ["ip"],
    [("127.0.0.1",), (None,)],
    ids=["exists", "absent"]
)


def test_empty_credentials(user, has_joined):
    assert cast[BadPayload](has_joined({}))
    assert cast[BadPayload](has_joined({"username": user.login}))
    assert cast[BadPayload](has_joined({"ip": "127.0.0.1"}))
    assert cast[BadPayload](has_joined({"serverId": uuid4()}))
    assert cast[BadPayload](has_joined({"username": user.login, "ip": "127.0.0.1"}))
    assert cast[BadPayload](has_joined({"ip": "127.0.0.1", "serverId": uuid4()}))


@optional_ip
def test_invalid_server(user, join, has_joined, ip: Optional[str]):
    join({
        "accessToken": user.access,
        "selectedProfile": user.uuid,
        "serverId": generate_server_id()
    })
    has_joined_response = has_joined({
        "username": user.login,
        "serverId": "anything",
        "ip": ip,
    })

    assert cast[InvalidServer](has_joined_response)


@optional_ip
def test_nonexistent_user(has_joined, ip: Optional[str]):
    response = has_joined({
        "username": "anything",
        "serverId": "anything",
        "ip": ip,
    })

    assert cast[InvalidProfile](response)


@optional_ip
def test_has_joined(user, join, has_joined, ip: Optional[str]):
    server_id = generate_server_id()
    join({
        "accessToken": user.access,
        "selectedProfile": user.uuid,
        "serverId": server_id
    })
    has_joined_response = has_joined({
        "username": user.login,
        "serverId": server_id,
        "ip": "127.0.0.2",
    })
    result = cast[JoinedResponse](has_joined_response)
    assert result is not None
    assert result.id == user.uuid
    assert result.name == user.login
