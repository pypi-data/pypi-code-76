from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel

from talar.resources.abstract import NestedResource

ApiKeyTypes = Literal["full", "publishable"]


class ApiKey(BaseModel):
    digest: str
    prefix: str
    name: str
    description: str
    type: ApiKeyTypes
    created_at: datetime


class ApiKeyCreate(ApiKey):
    token: str


class ApiKeys(NestedResource):
    resource = "api-keys/"

    def get(self, digest: str) -> ApiKey:
        return ApiKey(**self.client.get(f"{self.get_resource()}{digest}/"))

    def list(self) -> List[ApiKey]:
        output = self.client.get(self.get_resource())
        return [ApiKey(**key) for key in output]

    def delete(self, digest: str) -> None:
        return self.client.delete(f"{self.get_resource()}{digest}/")

    def update(
        self, digest: str, name: str, description: Optional[str] = None
    ) -> ApiKey:
        output = self.client.put(
            f"{self.get_resource()}{digest}/",
            data={"name": name, "description": description},
        )
        return ApiKey(**output)

    def create(
        self,
        name: str,
        key_type: ApiKeyTypes,
        description: Optional[str] = None,
    ) -> ApiKeyCreate:
        output = self.client.post(
            self.get_resource(),
            data={"name": name, "type": key_type, "description": description},
        )
        return ApiKeyCreate(**output)
