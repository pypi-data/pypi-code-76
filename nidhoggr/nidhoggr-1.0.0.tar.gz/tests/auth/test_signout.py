from nidhoggr.core.repository import BaseUserRepo
from nidhoggr.errors.auth import InvalidCredentials
from nidhoggr.errors.common import BadPayload
from ..conftest import cast


def test_empty_credentials(user, signout):
    assert cast[BadPayload](signout({}))
    assert cast[BadPayload](signout({"username": user.email}))
    assert cast[BadPayload](signout({"password": user.password}))


def test_nonexistent_user(signout):
    response = signout({
        "username": "unknown@ponyville.eq",
        "password": "anything"
    })
    assert response.status_code == 403
    assert cast[InvalidCredentials](response)


def test_wrong_password(user, signout):
    response = signout({
        "username": user.email,
        "password": "anything"
    })
    assert response.status_code == 403
    assert cast[InvalidCredentials](response)


def test_signout_full(users: BaseUserRepo, user, signout):
    response = signout({
        "username": user.email,
        "password": user.password,
    })
    assert response.status_code == 204
    assert response.data == b""
    fresh = users.get_user(uuid=user.uuid)
    assert fresh.access is None
