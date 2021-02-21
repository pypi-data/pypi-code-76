from uuid import uuid4, UUID

from nidhoggr.core.repository import BaseUserRepo
from nidhoggr.errors.auth import InvalidProfile
from nidhoggr.errors.common import BadPayload
from ..conftest import cast, generate_server_id


def test_empty_credentials(user, join):
    assert cast[BadPayload](join({}))
    assert cast[BadPayload](join({"accessToken": user.access}))
    assert cast[BadPayload](join({"selectedProfile": user.uuid}))
    assert cast[BadPayload](join({"serverId": uuid4()}))
    assert cast[BadPayload](join({"accessToken": user.access, "selectedProfile": user.uuid}))
    assert cast[BadPayload](join({"accessToken": user.access, "serverId": uuid4()}))
    assert cast[BadPayload](join({"selectedProfile": user.access, "serverId": uuid4()}))


def test_invalid_profile(user, join):
    response = join({
        "accessToken": user.access,
        "selectedProfile": UUID('df7e45e0-ebe4-40ad-a744-16ee1a04051f'),
        "serverId": uuid4()
    })
    assert cast[InvalidProfile](response)


def test_nonexistent_user(user, join):
    server_id = generate_server_id()
    response = join({
        "accessToken": UUID('0f2d2d09-5a4a-4e88-b774-bee307f6f107'),
        "selectedProfile": user.uuid,
        "serverId": server_id
    })

    assert cast[InvalidProfile](response)


def test_join(users: BaseUserRepo, user, join):
    server_id = generate_server_id()
    response = join({
        "accessToken": user.access,
        "selectedProfile": user.uuid,
        "serverId": server_id
    })
    assert response.status_code == 204
    assert response.data == b""
    fresh = users.get_user(uuid=user.uuid)
    assert fresh.server == server_id
