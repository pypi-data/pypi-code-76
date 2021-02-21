import pytest

from flask import url_for, Response
from flask.testing import FlaskClient

from nidhoggr.views import auth


def test_not_found(client: FlaskClient):
    response: Response = client.get("/unknown")
    assert response.status_code == 404


@pytest.mark.parametrize(["endpoint"], [(f,) for f in auth.__all__])
def test_get_method(client: FlaskClient, endpoint: str):
    response: Response = client.get(url_for(endpoint))
    assert response.status_code == 405
