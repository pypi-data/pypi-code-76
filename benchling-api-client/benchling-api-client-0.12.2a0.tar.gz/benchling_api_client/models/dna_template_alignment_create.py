from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dna_alignment_base_algorithm import DnaAlignmentBaseAlgorithm
from ..models.dna_alignment_base_files_item import DnaAlignmentBaseFilesItem
from ..models.dna_template_alignment_file import DnaTemplateAlignmentFile
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaTemplateAlignmentCreate")


@attr.s(auto_attribs=True)
class DnaTemplateAlignmentCreate:
    """  """

    template_sequence_id: str
    algorithm: DnaAlignmentBaseAlgorithm
    files: List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile]]
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        template_sequence_id = self.template_sequence_id
        algorithm = self.algorithm.value

        files = []
        for files_item_data in self.files:
            if isinstance(files_item_data, DnaAlignmentBaseFilesItem):
                files_item = files_item_data.to_dict()

            else:
                files_item = files_item_data.to_dict()

            files.append(files_item)

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "templateSequenceId": template_sequence_id,
                "algorithm": algorithm,
                "files": files,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        template_sequence_id = d.pop("templateSequenceId")

        algorithm = DnaAlignmentBaseAlgorithm(d.pop("algorithm"))

        files = []
        _files = d.pop("files")
        for files_item_data in _files:

            def _parse_files_item(
                data: Union[Dict[str, Any]]
            ) -> Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile]:
                files_item: Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile]
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    files_item = DnaAlignmentBaseFilesItem.from_dict(data)

                    return files_item
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                files_item = DnaTemplateAlignmentFile.from_dict(data)

                return files_item

            files_item = _parse_files_item(files_item_data)

            files.append(files_item)

        name = d.pop("name", UNSET)

        dna_template_alignment_create = cls(
            template_sequence_id=template_sequence_id,
            algorithm=algorithm,
            files=files,
            name=name,
        )

        return dna_template_alignment_create
