import json
from functools import wraps
from itertools import product
from pathlib import Path
from random import choice
from string import ascii_lowercase
from typing import Dict, Any, Union, Callable, TypeVar
from uuid import UUID, uuid4

import pytest
from flask import url_for, Response, Flask
from flask.testing import FlaskClient
from nidhoggr.core.response import StatusResponse, ErrorResponse, TextureStatusResponse

from nidhoggr.application import create_app
from nidhoggr.core.user import User
from nidhoggr.core.config import BLConfig
from nidhoggr.core.repository import BaseTextureRepo, BaseUserRepo
from nidhoggr.errors.common import YggdrasilError
from nidhoggr.models.auth import AuthenticationResponse, RefreshResponse
from nidhoggr.models.session import JoinedResponse
from nidhoggr.core.texture import TextureRequest, TextureUploadRequest, ComplexTextureResponse
from nidhoggr.utils.crypto import generate_keypair


class TestUser(User):
    # NOTE: Still needed for testing purposes
    password: str


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


USERS = list(map(
    TestUser.parse_obj,
    json.loads((Path(__file__).parent / "data/users.json").read_text())
))

EndpointCallable = Callable[[Dict[str, Any]], Response]
TEST_KEY_PAIR = generate_keypair()

YggdrasilResponse = Union[
    AuthenticationResponse,
    RefreshResponse,
    JoinedResponse,
]


def accessor(func: Callable):
    @wraps(func)
    def wrapper(client: FlaskClient, data: Dict[str, Any]):
        return client.post(
            url_for(func.__name__),
            data=json.dumps(data, cls=UUIDEncoder),
            content_type='application/json'
        )

    return wrapper


T = TypeVar("T")


class cast:
    def __getitem__(self, other) -> Callable[[T], Union[YggdrasilError, YggdrasilResponse]]:
        if isinstance(other, YggdrasilError):
            return lambda res: self[YggdrasilError](res) == other
        elif issubclass(other, YggdrasilError):
            return lambda res: other(status=res.status_code, **res.json)
        elif other in YggdrasilResponse.__args__:
            return lambda res: other(**res.json)
        else:
            return lambda res: None


cast = cast()


class TestUserRepo(BaseUserRepo):
    __users: Dict[int, TestUser]

    def __init__(self, *, users):
        self.__users = {user.uuid: user.copy() for user in users}

    def get_user(self, **kw: Dict[str, str]) -> Union[ErrorResponse, User]:
        res = [
            u
            for u
            in self.__users.values()
            if any(getattr(u, k) == v for k, v in kw.items())
        ]
        return (res or [BaseUserRepo.EMPTY_USER])[0]

    def save_user(self, *, user: TestUser) -> Union[ErrorResponse, User]:
        self.__users[user.uuid] = user
        return user

    def check_password(self, *, clean: str, uuid: str) -> Union[ErrorResponse, StatusResponse]:
        user = self.get_user(uuid=uuid)
        status = user and user.password == clean
        return StatusResponse(status=status)


# FIXME
class TestTextureRepo(BaseTextureRepo):
    def get(self, *, request: TextureRequest) -> Union[ErrorResponse, ComplexTextureResponse]:
        return ComplexTextureResponse(
            timestamp=0,
            profileId=uuid4(),
            profileName="",
            textures={}
        )

    def upload(self, *, request: TextureUploadRequest) -> Union[ErrorResponse, TextureStatusResponse]:
        return TextureStatusResponse(message="OK")

    def clear(self, *, request: TextureRequest) -> Union[ErrorResponse, TextureStatusResponse]:
        TextureStatusResponse(message="OK")


@pytest.fixture(params=list(product((False, True), (False, True))))
def config(request) -> BLConfig:
    strict, simple_login, *_ = request.param
    return BLConfig(
        key_pair=TEST_KEY_PAIR,
        strict=strict,
        simple_login=simple_login,
    )


@pytest.fixture
def users() -> TestUserRepo:
    return TestUserRepo(users=USERS)


@pytest.fixture
def textures() -> TestTextureRepo:
    return TestTextureRepo()


@pytest.fixture(autouse=True)
def skip_bl(request, config):
    if request.node.get_closest_marker("skip_bl_on"):
        marker = request.node.get_closest_marker("skip_bl_on")
        if any(
            marker.kwargs.get(name, ...) == value
            for name, value
            in config._asdict().items()
        ):
            pytest.skip(f"Skipped on {config}")


@pytest.fixture
def user(users) -> User:
    return users.get_user(uuid=UUID("3388364d-4e96-4567-aaf9-3d113cdef2af"))


@pytest.fixture
def old_user(users) -> User:
    return users.get_user(uuid=UUID("0b6b2656-73fb-41ce-b116-c3c4cc5753c4"))


@pytest.fixture
def new_user(users) -> User:
    return users.get_user(uuid=UUID("3ad95d5d-7986-4464-837f-dd6dd7444ed5"))


@pytest.fixture
def app(
    users,
    config: BLConfig,
    textures: BaseTextureRepo
) -> Flask:
    return create_app(
        users=users,
        config=config,
        textures=textures,
    )


def generate_server_id() -> str:
    return ''.join(choice(ascii_lowercase) for i in range(40))
