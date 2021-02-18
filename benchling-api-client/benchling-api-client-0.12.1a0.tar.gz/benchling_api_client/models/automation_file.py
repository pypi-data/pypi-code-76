from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.automation_file_automation_file_config import AutomationFileAutomationFileConfig
from ..models.automation_file_file import AutomationFileFile
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutomationFile")


@attr.s(auto_attribs=True)
class AutomationFile:
    """  """

    id: str
    assay_run_id: Union[Unset, str] = UNSET
    automation_file_config: Union[Unset, AutomationFileAutomationFileConfig] = UNSET
    file: Union[Unset, None, AutomationFileFile] = UNSET
    status: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        assay_run_id = self.assay_run_id
        automation_file_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.automation_file_config, Unset):
            automation_file_config = self.automation_file_config.to_dict()

        file: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_dict() if self.file else None

        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )
        if assay_run_id is not UNSET:
            field_dict["assayRunId"] = assay_run_id
        if automation_file_config is not UNSET:
            field_dict["automationFileConfig"] = automation_file_config
        if file is not UNSET:
            field_dict["file"] = file
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        assay_run_id = d.pop("assayRunId", UNSET)

        automation_file_config: Union[Unset, AutomationFileAutomationFileConfig] = UNSET
        _automation_file_config = d.pop("automationFileConfig", UNSET)
        if not isinstance(_automation_file_config, Unset):
            automation_file_config = AutomationFileAutomationFileConfig.from_dict(_automation_file_config)

        file = None
        _file = d.pop("file", UNSET)
        if _file is not None and not isinstance(_file, Unset):
            file = AutomationFileFile.from_dict(_file)

        status = d.pop("status", UNSET)

        automation_file = cls(
            id=id,
            assay_run_id=assay_run_id,
            automation_file_config=automation_file_config,
            file=file,
            status=status,
        )

        return automation_file
