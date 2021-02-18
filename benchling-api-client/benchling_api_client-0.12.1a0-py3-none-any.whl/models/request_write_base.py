import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.fields import Fields
from ..models.request_sample_group import RequestSampleGroup
from ..models.request_task import RequestTask
from ..models.request_write_team_assignee import RequestWriteTeamAssignee
from ..models.request_write_user_assignee import RequestWriteUserAssignee
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestWriteBase")


@attr.s(auto_attribs=True)
class RequestWriteBase:
    """  """

    assignees: Union[Unset, List[Union[RequestWriteUserAssignee, RequestWriteTeamAssignee]]] = UNSET
    requestor_id: Union[Unset, None, str] = UNSET
    scheduled_on: Union[Unset, datetime.date] = UNSET
    project_id: Union[Unset, str] = UNSET
    sample_groups: Union[Unset, List[RequestSampleGroup]] = UNSET
    tasks: Union[Unset, List[RequestTask]] = UNSET
    fields: Union[Unset, Fields] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        assignees: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.assignees, Unset):
            assignees = []
            for assignees_item_data in self.assignees:
                if isinstance(assignees_item_data, RequestWriteUserAssignee):
                    assignees_item = assignees_item_data.to_dict()

                else:
                    assignees_item = assignees_item_data.to_dict()

                assignees.append(assignees_item)

        requestor_id = self.requestor_id
        scheduled_on: Union[Unset, str] = UNSET
        if not isinstance(self.scheduled_on, Unset):
            scheduled_on = self.scheduled_on.isoformat()

        project_id = self.project_id
        sample_groups: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.sample_groups, Unset):
            sample_groups = []
            for sample_groups_item_data in self.sample_groups:
                sample_groups_item = sample_groups_item_data.to_dict()

                sample_groups.append(sample_groups_item)

        tasks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = []
            for tasks_item_data in self.tasks:
                tasks_item = tasks_item_data.to_dict()

                tasks.append(tasks_item)

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if assignees is not UNSET:
            field_dict["assignees"] = assignees
        if requestor_id is not UNSET:
            field_dict["requestorId"] = requestor_id
        if scheduled_on is not UNSET:
            field_dict["scheduledOn"] = scheduled_on
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if sample_groups is not UNSET:
            field_dict["sampleGroups"] = sample_groups
        if tasks is not UNSET:
            field_dict["tasks"] = tasks
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assignees = []
        _assignees = d.pop("assignees", UNSET)
        for assignees_item_data in _assignees or []:

            def _parse_assignees_item(
                data: Union[Dict[str, Any]]
            ) -> Union[RequestWriteUserAssignee, RequestWriteTeamAssignee]:
                assignees_item: Union[RequestWriteUserAssignee, RequestWriteTeamAssignee]
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    assignees_item = RequestWriteUserAssignee.from_dict(data)

                    return assignees_item
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                assignees_item = RequestWriteTeamAssignee.from_dict(data)

                return assignees_item

            assignees_item = _parse_assignees_item(assignees_item_data)

            assignees.append(assignees_item)

        requestor_id = d.pop("requestorId", UNSET)

        scheduled_on = None
        _scheduled_on = d.pop("scheduledOn", UNSET)
        if _scheduled_on is not None:
            scheduled_on = isoparse(cast(str, _scheduled_on)).date()

        project_id = d.pop("projectId", UNSET)

        sample_groups = []
        _sample_groups = d.pop("sampleGroups", UNSET)
        for sample_groups_item_data in _sample_groups or []:
            sample_groups_item = RequestSampleGroup.from_dict(sample_groups_item_data)

            sample_groups.append(sample_groups_item)

        tasks = []
        _tasks = d.pop("tasks", UNSET)
        for tasks_item_data in _tasks or []:
            tasks_item = RequestTask.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        fields: Union[Unset, Fields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = Fields.from_dict(_fields)

        request_write_base = cls(
            assignees=assignees,
            requestor_id=requestor_id,
            scheduled_on=scheduled_on,
            project_id=project_id,
            sample_groups=sample_groups,
            tasks=tasks,
            fields=fields,
        )

        return request_write_base
