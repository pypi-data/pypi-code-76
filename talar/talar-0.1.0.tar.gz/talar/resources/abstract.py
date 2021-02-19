from typing import Optional

from talar.client import Client


class Resource:
    resource = NotImplemented

    def __init__(self, client: Client):
        self.client = client

    def get_resource(self) -> str:
        return self.resource


class NestedResource(Resource):
    def __init__(self, parent: Resource, client: Optional[Client] = None):
        super().__init__(client if client else parent.client)
        self.parent = parent

    def get_resource(self) -> str:
        return f"{self.parent.get_resource()}{self.resource}"
