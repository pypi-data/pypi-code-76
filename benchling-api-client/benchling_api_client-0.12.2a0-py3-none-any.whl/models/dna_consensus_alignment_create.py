from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dna_alignment_base_algorithm import DnaAlignmentBaseAlgorithm
from ..models.dna_alignment_base_files_item import DnaAlignmentBaseFilesItem
from ..models.dna_consensus_alignment_create_new_sequence import DnaConsensusAlignmentCreateNewSequence
from ..models.dna_template_alignment_file import DnaTemplateAlignmentFile
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaConsensusAlignmentCreate")


@attr.s(auto_attribs=True)
class DnaConsensusAlignmentCreate:
    """  """

    algorithm: DnaAlignmentBaseAlgorithm
    files: List[Union[DnaAlignmentBaseFilesItem, DnaTemplateAlignmentFile]]
    new_sequence: Union[Unset, DnaConsensusAlignmentCreateNewSequence] = UNSET
    sequence_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        algorithm = self.algorithm.value

        files = []
        for files_item_data in self.files:
            if isinstance(files_item_data, DnaAlignmentBaseFilesItem):
                files_item = files_item_data.to_dict()

            else:
                files_item = files_item_data.to_dict()

            files.append(files_item)

        new_sequence: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.new_sequence, Unset):
            new_sequence = self.new_sequence.to_dict()

        sequence_id = self.sequence_id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "algorithm": algorithm,
                "files": files,
            }
        )
        if new_sequence is not UNSET:
            field_dict["newSequence"] = new_sequence
        if sequence_id is not UNSET:
            field_dict["sequenceId"] = sequence_id
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
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

        new_sequence: Union[Unset, DnaConsensusAlignmentCreateNewSequence] = UNSET
        _new_sequence = d.pop("newSequence", UNSET)
        if not isinstance(_new_sequence, Unset):
            new_sequence = DnaConsensusAlignmentCreateNewSequence.from_dict(_new_sequence)

        sequence_id = d.pop("sequenceId", UNSET)

        name = d.pop("name", UNSET)

        dna_consensus_alignment_create = cls(
            algorithm=algorithm,
            files=files,
            new_sequence=new_sequence,
            sequence_id=sequence_id,
            name=name,
        )

        return dna_consensus_alignment_create
