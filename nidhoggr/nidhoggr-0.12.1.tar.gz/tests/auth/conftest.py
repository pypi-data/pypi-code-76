from functools import partial
from uuid import UUID

import pytest
from flask.testing import FlaskClient

from nidhoggr.views import auth
from ..conftest import accessor, EndpointCallable


@pytest.fixture
def authenticate(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.authenticate), client)


@pytest.fixture
def refresh(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.refresh), client)


@pytest.fixture
def validate(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.validate), client)


@pytest.fixture
def invalidate(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.invalidate), client)


@pytest.fixture
def signout(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.signout), client)


def check_uuid(uuid):
    assert isinstance(uuid, UUID)
