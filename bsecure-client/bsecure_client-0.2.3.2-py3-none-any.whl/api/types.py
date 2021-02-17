import datetime as dt
from typing import Optional, Union

import pydantic

from ..utils import File


def to_camel(snake_str: str) -> str:
    first, *others = snake_str.split("_")
    ret = "".join([first.lower(), *map(str.title, others)])
    return ret


class BaseAPIModel(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True
        alias_generator = to_camel
        allow_population_by_field_name = True

    def dict(self, **kwargs):
        """Returns camelCased version and removes any non specified optional fields """
        return super().dict(by_alias=True, exclude_unset=True)


class PatchAssetInput(BaseAPIModel):
    category: Optional[str]
    code: Optional[str]
    photo: Union[File, str, None]
    make: Optional[str]
    model: Optional[str]
    size: Optional[str]
    location: Optional[str]
    status: Optional[str]
    condition: Optional[str]
    installation_timestamp: Optional[dt.datetime]
    expected_life_years: Optional[dt.datetime]


class PatchRemarkInput(BaseAPIModel):
    resolved_timestamp: Optional[dt.datetime]
    description: Optional[str]
    severity: Optional[str]
    resolution: Optional[str]


class PatchServiceInput(BaseAPIModel):
    name: Optional[str]
    due_date: Optional[dt.date]
    performed_timestamp: Optional[dt.datetime]
    description: Optional[str]
    result: Optional[str]


class PatchTenantDocumentInput(BaseAPIModel):
    title: Optional[str]
