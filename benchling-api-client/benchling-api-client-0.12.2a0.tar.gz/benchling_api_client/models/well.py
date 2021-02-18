import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.container_content import ContainerContent
from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..models.well_schema import WellSchema
from ..models.well_volume import WellVolume
from ..types import UNSET, Unset

T = TypeVar("T", bound="Well")


@attr.s(auto_attribs=True)
class Well:
    """  """

    fields: Fields
    id: str
    barcode: Union[Unset, str] = UNSET
    contents: Union[Unset, List[ContainerContent]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, UserSummary] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET
    parent_storage_schema: Union[Unset, SchemaSummary] = UNSET
    project_id: Union[Unset, None, str] = UNSET
    schema: Union[Unset, None, WellSchema] = UNSET
    volume: Union[Unset, WellVolume] = UNSET
    web_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields = self.fields.to_dict()

        id = self.id
        barcode = self.barcode
        contents: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.contents, Unset):
            contents = []
            for contents_item_data in self.contents:
                contents_item = contents_item_data.to_dict()

                contents.append(contents_item)

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        name = self.name
        parent_storage_id = self.parent_storage_id
        parent_storage_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parent_storage_schema, Unset):
            parent_storage_schema = self.parent_storage_schema.to_dict()

        project_id = self.project_id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict() if self.schema else None

        volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.volume, Unset):
            volume = self.volume.to_dict()

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
                "id": id,
            }
        )
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if contents is not UNSET:
            field_dict["contents"] = contents
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id
        if parent_storage_schema is not UNSET:
            field_dict["parentStorageSchema"] = parent_storage_schema
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if volume is not UNSET:
            field_dict["volume"] = volume
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id")

        barcode = d.pop("barcode", UNSET)

        contents = []
        _contents = d.pop("contents", UNSET)
        for contents_item_data in _contents or []:
            contents_item = ContainerContent.from_dict(contents_item_data)

            contents.append(contents_item)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        creator: Union[Unset, UserSummary] = UNSET
        _creator = d.pop("creator", UNSET)
        if not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(_creator)

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        name = d.pop("name", UNSET)

        parent_storage_id = d.pop("parentStorageId", UNSET)

        parent_storage_schema: Union[Unset, SchemaSummary] = UNSET
        _parent_storage_schema = d.pop("parentStorageSchema", UNSET)
        if not isinstance(_parent_storage_schema, Unset):
            parent_storage_schema = SchemaSummary.from_dict(_parent_storage_schema)

        project_id = d.pop("projectId", UNSET)

        schema = None
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = WellSchema.from_dict(_schema)

        volume: Union[Unset, WellVolume] = UNSET
        _volume = d.pop("volume", UNSET)
        if not isinstance(_volume, Unset):
            volume = WellVolume.from_dict(_volume)

        web_url = d.pop("webURL", UNSET)

        well = cls(
            fields=fields,
            id=id,
            barcode=barcode,
            contents=contents,
            created_at=created_at,
            creator=creator,
            modified_at=modified_at,
            name=name,
            parent_storage_id=parent_storage_id,
            parent_storage_schema=parent_storage_schema,
            project_id=project_id,
            schema=schema,
            volume=volume,
            web_url=web_url,
        )

        return well
