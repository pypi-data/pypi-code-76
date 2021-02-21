from functools import partial

import pytest
from flask.testing import FlaskClient

from nidhoggr.core.config import BLConfig
from nidhoggr.views import session, legacy
from ..conftest import accessor, accessor_legacy, EndpointCallable


@pytest.fixture
def join(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(session.join), client)


@pytest.fixture
def has_joined(client: FlaskClient, config: BLConfig) -> EndpointCallable:
    if config.legacy_compat:
        return partial(accessor_legacy(legacy.hasJoined), client)
    else:
        return partial(accessor(session.has_joined), client)


@pytest.fixture
def profile(client: FlaskClient, config: BLConfig) -> EndpointCallable:
    if config.legacy_compat:
        return partial(accessor_legacy(legacy.profile), client)
    else:
        return partial(accessor(session.profile), client)
