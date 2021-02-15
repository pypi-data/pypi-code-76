from typing import Any, Dict, List, Optional, Tuple

from pydantic import Field
from pydantic.types import constr

from kelvin.sdk.lib.common.configs.internal.datamodel_configs import DatamodelConfigs
from kelvin.sdk.lib.common.exceptions import DataModelException
from kelvin.sdk.lib.common.models.generic import KSDKModel


class ICDField(KSDKModel):
    description: str
    name: str
    type: str
    array: Optional[bool]


class ICDPayloadHelper(KSDKModel):
    name: constr(regex=DatamodelConfigs.datamodel_name_acceptance_regex)  # type: ignore # noqa
    class_name: constr(regex=DatamodelConfigs.datamodel_class_name_acceptance_regex)  # type: ignore # noqa
    description: str
    payload_fields: List[ICDField] = Field(..., alias="fields")
    version: str

    class Config:
        allow_population_by_field_name: bool = True

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return super().dict(by_alias=True, *args, **kwargs)

    @property
    def datamodel_file_name(self) -> str:
        """
        Based on the data model name and its version, get the project specific file name.

        :return: the name of the file that will be created to host the new datamodel

        """

        if not self.name or not self.version:
            raise DataModelException("Datamodel requires both a name and a version")

        name: str = self.name.replace(".", "_")
        version: str = self.version.replace(".", "-")

        return f"{name}__{version}{DatamodelConfigs.datamodel_default_icd_extension}"

    @property
    def full_datamodel_name(self) -> str:
        return f"{self.name}:{self.version}"

    @property
    def dependency_datamodels(self) -> List[Tuple[str, str]]:
        return_obj = []
        for item in self.payload_fields:
            if item.type and item.type.count(":") == 1:
                name, version = item.type.split(":", 1)
                return_obj.append((name, version))
        return list(set(return_obj))
