import datetime
from typing import Any, Dict, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="WarehouseCredentials")


@attr.s(auto_attribs=True)
class WarehouseCredentials:
    """  """

    expires_at: datetime.datetime
    username: str
    password: str

    def to_dict(self) -> Dict[str, Any]:
        expires_at = self.expires_at.isoformat()

        username = self.username
        password = self.password

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expiresAt": expires_at,
                "username": username,
                "password": password,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expires_at = isoparse(d.pop("expiresAt"))

        username = d.pop("username")

        password = d.pop("password")

        warehouse_credentials = cls(
            expires_at=expires_at,
            username=username,
            password=password,
        )

        return warehouse_credentials
