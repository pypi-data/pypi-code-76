import datetime
from typing import Any, Dict, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.sample_group import SampleGroup
from ..models.sample_group_status import SampleGroupStatus

T = TypeVar("T", bound="RequestFulfillment")


@attr.s(auto_attribs=True)
class RequestFulfillment:
    """A request fulfillment represents work that is done which changes the status of a request or a sample group within that request.
    Fulfillments are created when state changes between IN_PROGRESS, COMPLETED, or FAILED statuses. Fulfillments do not capture a PENDING state because all requests or request sample groups are considered PENDING until the first corresponding fulfillment is created.
    """

    id: str
    created_at: datetime.datetime
    entry_id: str
    request_id: str
    status: SampleGroupStatus
    sample_group: SampleGroup

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at = self.created_at.isoformat()

        entry_id = self.entry_id
        request_id = self.request_id
        status = self.status.value

        sample_group = self.sample_group.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "createdAt": created_at,
                "entryId": entry_id,
                "requestId": request_id,
                "status": status,
                "sampleGroup": sample_group,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("createdAt"))

        entry_id = d.pop("entryId")

        request_id = d.pop("requestId")

        status = SampleGroupStatus(d.pop("status"))

        sample_group = SampleGroup.from_dict(d.pop("sampleGroup"))

        request_fulfillment = cls(
            id=id,
            created_at=created_at,
            entry_id=entry_id,
            request_id=request_id,
            status=status,
            sample_group=sample_group,
        )

        return request_fulfillment
