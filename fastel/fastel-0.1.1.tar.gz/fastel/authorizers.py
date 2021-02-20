from __future__ import annotations

from typing import Optional

from jwt.exceptions import DecodeError
from mongoengine import BaseDocument  # type: ignore
from revjwt import decode  # type: ignore

from . import exceptions


class Credential:
    def __init__(self, client: Optional[BaseDocument] = None, user=None):
        self.client = client
        self.user = user


class BaseAuth:
    client_model_class: BaseDocument

    def __init__(self, force: bool = False):
        self.force = force

    def __or__(self, other: BaseAuth):
        return OR(self, other)

    def __call__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Optional[Credential]:
        return self.verify(
            client_id=client_id, token=token, client_secret=client_secret
        )

    def verify(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Optional[Credential]:
        raise NotImplementedError("verify() should be implemented")


class ClientIdAuth(BaseAuth):
    def __init__(self, force: bool = False):
        super().__init__(force)
        if self.client_model_class is None:
            raise ValueError("client_model_class should not be None")

    def verify(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Optional[Credential]:
        if not client_id and self.force:
            raise exceptions.APIException(
                status_code=403, error="access_denied", detail="client_id is required"
            )
        if not client_id:
            return None
        try:
            client = self.client_model_class.objects.get(id=client_id)
        except self.client_model_class.DoesNotExist as exc:
            raise exceptions.APIException(
                status_code=403, error="access_denied", detail=f"{client_id} not found"
            ) from exc
        return Credential(client=client)


class JWBaseAuth(BaseAuth):
    expected_aud: Optional[str] = None

    def verify(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Optional[Credential]:
        if not token and self.force:
            raise exceptions.APIException(
                status_code=403, error="permission_denied", detail="token is required"
            )
        if not token:
            return None

        try:
            decoded = decode(token)
        except DecodeError as exc:
            raise exceptions.APIException(
                status_code=403, error="permission_denied", detail=exc
            )

        if self.expected_aud and decoded["aud"] != self.expected_aud:
            raise exceptions.APIException(
                status_code=403,
                error="permission_denied",
                detail=f"required aud: {self.expected_aud}",
            )

        if self.client_model_class:
            try:
                client = self.client_model_class.objects.get(id=decoded["aud"])
            except self.client_model_class.DoesNotExist as exc:
                raise exceptions.APIException(
                    status_code=403,
                    error="permission_denied",
                    detail=f"{client_id} not found",
                ) from exc
        else:
            client = None
        return Credential(client=client, user=decoded)


class ClientSecretAuth(BaseAuth):
    def __init__(self, force: bool = False):
        super().__init__(force)
        if self.client_model_class is None:
            raise ValueError("client_model_class should not be None")

    def verify(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Optional[Credential]:

        try:
            client = self.client_model_class.get(id=client_id)
            return Credential(client=client)
        except self.client_model_class.DoesNotExist as exc:
            raise exceptions.APIException(
                status_code=403,
                error="permission_denied",
                detail=f"{client_id} not found",
            ) from exc

        if client.client_secret != client_secret:
            raise exceptions.APIException(
                status_code=403,
                error="permission_denied",
                detail="client_sercet not match",
            )

        return Credential(client=client)


class OR(BaseAuth):
    def __init__(self, left: BaseAuth, right: BaseAuth):
        super().__init__()
        self.left = left
        self.right = right

    def verify(self, *args, **kwargs) -> Optional[Credential]:
        result = self.left(*args, **kwargs)
        if not result:
            result = self.right(*args, **kwargs)
        return result
