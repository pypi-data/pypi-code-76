from typing import Union

from pydantic import BaseModel, HttpUrl

from talar.client import Client
from talar.resources.abstract import Resource


class Project(BaseModel):
    id: str
    name: str
    url: Union[HttpUrl, str]


class Projects(Resource):
    resource = "projects/"

    def __init__(self, project_id: str, client: Client):
        super().__init__(client)
        self.project_id = project_id

    def get_resource(self) -> str:
        return f"{self.resource}{self.project_id}/"

    def get(self) -> Project:
        return Project(**self.client.get(self.get_resource()))
