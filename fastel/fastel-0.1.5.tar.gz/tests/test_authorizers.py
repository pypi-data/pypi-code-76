from typing import Any
from unittest.mock import patch

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from fastel.authorizers import ClientIdAuth, ClientSecretAuth, Credential, JWBaseAuth
from fastel.exceptions import APIException, api_exception_handler

MOCK_DECODE_PATH = "revjwt.decode"

CLIENT_AUTH_PATH = "/test-client-auth"
CLIENT_SECRET_PATH = "/test-secret-auth"
JWT_AUTH_PATH = "/test-jwt-auth"
CLIENTLESS_JWT_AUTH_PATH = "/test-clientless-jwt"
MULTI_AUTH = "/test-multi-auth"
NOTFOUND_JWT_AUTH = "/test-notfound-jwt"
NOTFORCE_JWT_AUTH = "/test-notforce-jwt"

app = FastAPI()
app.exception_handler(APIException)(api_exception_handler)


class ClientInstance:
    client_id = "test"
    client_secret = "secret123"


class FakeClient:
    DoesNotExist = Exception

    class objects:
        @classmethod
        def get(self, *args: Any, **kwargs: Any) -> ClientInstance:
            if kwargs.get("client_id") == "not_found":
                raise FakeClient.DoesNotExist()
            return ClientInstance()


class ClientAuth(ClientIdAuth):
    client_model_class = FakeClient


class SecretAuth(ClientSecretAuth):
    client_model_class = FakeClient


class JWTAuth(JWBaseAuth):
    client_model_class = FakeClient
    expected_aud = "test"


class ClientlessJWTAuth(JWBaseAuth):
    pass


class NotFoundJWTAuth(JWBaseAuth):
    client_model_class = FakeClient
    expected_aud = "not_found"


@app.get(CLIENT_AUTH_PATH)
def get_client(
    credential: Credential = Depends(ClientAuth(force=True)),
) -> Any:
    return {"client_id": credential.client.client_id}


@app.get(CLIENT_SECRET_PATH)
def get_secret(
    credential: Credential = Depends(SecretAuth(force=True)),
) -> Any:
    return {"client_id": credential.client.client_id}


@app.get(JWT_AUTH_PATH)
def get_jwt(
    credential: Credential = Depends(JWTAuth(force=True)),
) -> Any:
    return {"client_id": credential.client.client_id}


@app.get(NOTFORCE_JWT_AUTH)
def get_notforce_jwt(
    credential: Credential = Depends(JWTAuth()),
) -> Any:
    if not credential:
        return {"client_id": "not_force"}


@app.get(NOTFOUND_JWT_AUTH)
def get_notfound_jwt(
    credential: Credential = Depends(NotFoundJWTAuth(force=True)),
) -> Any:
    pass  # pragma: no cover


@app.get(MULTI_AUTH)
def get_multi(
    credential: Credential = Depends(ClientAuth() | SecretAuth() | JWTAuth(force=True)),
) -> Any:
    return {"client_id": credential.client.client_id}


@app.get(CLIENTLESS_JWT_AUTH_PATH)
def get_clientless(
    credential: Credential = Depends(ClientlessJWTAuth(force=True)),
) -> Any:
    if not credential.client:
        return {"client": None}
    return {"client": "exist"}  # pragma: no cover


client = TestClient(app)


def test_client_auth() -> None:
    response = client.get(CLIENT_AUTH_PATH)
    assert response.status_code == 403

    response = client.get(f"{CLIENT_AUTH_PATH}?client_id=not_found")
    assert response.status_code == 403

    response = client.get(f"{CLIENT_AUTH_PATH}?client_id=test")
    assert response.status_code == 200
    assert response.json()["client_id"] == "test"


def test_secret_auth() -> None:
    response = client.get(CLIENT_SECRET_PATH)
    assert response.status_code == 403

    response = client.get(
        f"{CLIENT_SECRET_PATH}?client_id=test&client_secret=wrongsecret"
    )
    assert response.status_code == 403

    response = client.get(
        f"{CLIENT_SECRET_PATH}?client_id=not_found&client_secret=wrongsecret"
    )
    assert response.status_code == 403

    response = client.get(
        f"{CLIENT_SECRET_PATH}?client_id=teset&client_secret=secret123"
    )
    assert response.status_code == 200
    assert response.json()["client_id"] == "test"


def test_jwt_auth() -> None:
    response = client.get(JWT_AUTH_PATH)
    assert response.status_code == 403

    response = client.get(f"{JWT_AUTH_PATH}?token=foo")
    assert response.status_code == 403

    response = client.get(f"{NOTFORCE_JWT_AUTH}")
    assert response.status_code == 200
    assert response.json()["client_id"] == "not_force"

    with patch(MOCK_DECODE_PATH) as decode:
        decode.return_value = {"aud": "test"}
        response = client.get(f"{JWT_AUTH_PATH}?token=foo")
        assert response.status_code == 200

        response = client.get(f"{CLIENTLESS_JWT_AUTH_PATH}?token=foo")
        assert response.status_code == 200
        assert response.json()["client"] is None

    with patch(MOCK_DECODE_PATH) as decode:
        decode.return_value = {"aud": "error-aud"}
        response = client.get(f"{JWT_AUTH_PATH}?token=foo")
        assert response.status_code == 403

    with patch(MOCK_DECODE_PATH) as decode:
        decode.return_value = {"aud": "not_found"}
        response = client.get(f"{NOTFOUND_JWT_AUTH}?token=foo")
        assert response.status_code == 403

    response = client.get(CLIENTLESS_JWT_AUTH_PATH)
    assert response.status_code == 403


def test_multi_auth() -> None:
    response = client.get(MULTI_AUTH)
    assert response.status_code == 403
    assert response.json()["detail"] == "token is required"

    response = client.get(f"{MULTI_AUTH}?client_id=test")
    assert response.status_code == 200

    response = client.get(f"{MULTI_AUTH}?client_id=test&client_secret=secret123")
    assert response.status_code == 200

    with patch(MOCK_DECODE_PATH) as decode:
        decode.return_value = {"aud": "test"}
        response = client.get(f"{MULTI_AUTH}?token=foo")
        assert response.status_code == 200
