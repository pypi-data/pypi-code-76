from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Optional as Opt

from simio.utils import deep_merge_dicts


@dataclass
class AbstractSwagger(ABC):
    """
    Base class for swagger entities

    Has abstract method json
    """

    @abstractmethod
    def json(self) -> dict:
        ...


@dataclass
class SwaggerResponse(AbstractSwagger):
    code: int
    description: str

    def json(self) -> dict:
        return {str(self.code): {"description": self.description}}


@dataclass
class SwaggerProperty(AbstractSwagger):
    type: str
    name: Opt[str] = None
    items: Opt["SwaggerProperty"] = None
    properties: List["SwaggerProperty"] = field(default_factory=list)

    def json(self) -> dict:
        json_ = {"type": self.type}
        if self.items is not None:
            json_["items"] = self.items.json()
        elif len(self.properties) != 0:
            json_["properties"] = _list_to_dict(self.properties)

        if self.name is not None:
            json_ = {self.name: json_}

        return json_


@dataclass
class SwaggerParameter(AbstractSwagger):
    in_: str
    name: str
    required: Opt[bool] = None
    schema: Opt[SwaggerProperty] = None
    type: Opt[str] = None

    def json(self) -> dict:
        json_swagger = {
            "in": self.in_,
            "name": self.name,
        }
        if self.schema is not None:
            json_swagger["schema"] = self.schema.json()
        if self.required is not None:
            json_swagger["required"] = self.required
        if self.type is not None:
            json_swagger["type"] = self.type

        return json_swagger


@dataclass
class SwaggerMethod(AbstractSwagger):
    method: str
    tags: List[str] = field(default_factory=list)
    parameters: List[SwaggerParameter] = field(default_factory=list)
    responses: List[SwaggerResponse] = field(default_factory=list)

    def json(self) -> dict:
        return {
            self.method: {
                "tags": self.tags,
                "parameters": [parameter.json() for parameter in self.parameters],
                "responses": _list_to_dict(self.responses),
            }
        }


@dataclass
class SwaggerPath(AbstractSwagger):
    path: str
    methods: List[SwaggerMethod] = field(default_factory=list)

    def json(self) -> dict:
        return {self.path: _list_to_dict(self.methods)}


@dataclass
class SwaggerInfo(AbstractSwagger):
    version: str
    title: str

    def json(self) -> dict:
        return self.__dict__


@dataclass
class SwaggerConfig:
    info: SwaggerInfo
    paths: List[SwaggerPath] = field(default_factory=list)
    version: str = "2.0"

    def json(self):
        return {
            "swagger": self.version,
            "info": self.info.json(),
            "paths": _list_to_dict(self.paths),
        }


def _list_to_dict(swagger_elements: List[AbstractSwagger]):
    dictionary = {}

    for element in swagger_elements:
        dictionary = deep_merge_dicts(dictionary, element.json())

    return dictionary
