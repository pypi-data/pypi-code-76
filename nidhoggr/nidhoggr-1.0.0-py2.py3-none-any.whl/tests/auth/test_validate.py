from uuid import UUID

from nidhoggr.errors.auth import InvalidAccessToken, InvalidClientToken
from nidhoggr.errors.common import BadPayload
from ..conftest import cast


def test_empty_credentials(user, validate):
    assert cast[BadPayload](validate({}))
    assert cast[BadPayload](validate({"clientToken": user.client}))


def test_broken_access_token(user, validate):
    response = validate({
        "accessToken": UUID('04ee4899-880d-4a36-b6de-d62cd581328d'),
        "clientToken": user.client
    })
    assert response.status_code == 403
    assert cast[InvalidAccessToken](response)


def test_invalid_client_token(user, validate):
    response = validate({
        "accessToken": user.access,
        "clientToken": UUID('30e4b8ed-e8d4-4e6f-b651-e4d700a4606c')
    })
    assert response.status_code == 403
    assert cast[InvalidClientToken](response)


def test_validate_full(user, validate):
    response = validate({
        "accessToken": user.access,
        "clientToken": user.client
    })
    assert response.status_code == 204
    assert response.data == b""


def test_validate_simple(user, validate):
    response = validate({
        "accessToken": user.access,
    })
    assert response.status_code == 204
    assert response.data == b""
