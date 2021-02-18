from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectsArchivalChange")


@attr.s(auto_attribs=True)
class ProjectsArchivalChange:
    """IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of projects along with any IDs of project contents that were unarchived."""

    project_ids: Union[Unset, List[str]] = UNSET
    folder_ids: Union[Unset, List[str]] = UNSET
    entry_ids: Union[Unset, List[str]] = UNSET
    protocol_ids: Union[Unset, List[str]] = UNSET
    dna_sequence_ids: Union[Unset, List[str]] = UNSET
    aa_sequence_ids: Union[Unset, List[str]] = UNSET
    custom_entity_ids: Union[Unset, List[str]] = UNSET
    mixture_ids: Union[Unset, List[str]] = UNSET
    oligo_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        project_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.project_ids, Unset):
            project_ids = self.project_ids

        folder_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.folder_ids, Unset):
            folder_ids = self.folder_ids

        entry_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.entry_ids, Unset):
            entry_ids = self.entry_ids

        protocol_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.protocol_ids, Unset):
            protocol_ids = self.protocol_ids

        dna_sequence_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.dna_sequence_ids, Unset):
            dna_sequence_ids = self.dna_sequence_ids

        aa_sequence_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aa_sequence_ids, Unset):
            aa_sequence_ids = self.aa_sequence_ids

        custom_entity_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.custom_entity_ids, Unset):
            custom_entity_ids = self.custom_entity_ids

        mixture_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.mixture_ids, Unset):
            mixture_ids = self.mixture_ids

        oligo_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.oligo_ids, Unset):
            oligo_ids = self.oligo_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if project_ids is not UNSET:
            field_dict["projectIds"] = project_ids
        if folder_ids is not UNSET:
            field_dict["folderIds"] = folder_ids
        if entry_ids is not UNSET:
            field_dict["entryIds"] = entry_ids
        if protocol_ids is not UNSET:
            field_dict["protocolIds"] = protocol_ids
        if dna_sequence_ids is not UNSET:
            field_dict["dnaSequenceIds"] = dna_sequence_ids
        if aa_sequence_ids is not UNSET:
            field_dict["aaSequenceIds"] = aa_sequence_ids
        if custom_entity_ids is not UNSET:
            field_dict["customEntityIds"] = custom_entity_ids
        if mixture_ids is not UNSET:
            field_dict["mixtureIds"] = mixture_ids
        if oligo_ids is not UNSET:
            field_dict["oligoIds"] = oligo_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_ids = cast(List[str], d.pop("projectIds", UNSET))

        folder_ids = cast(List[str], d.pop("folderIds", UNSET))

        entry_ids = cast(List[str], d.pop("entryIds", UNSET))

        protocol_ids = cast(List[str], d.pop("protocolIds", UNSET))

        dna_sequence_ids = cast(List[str], d.pop("dnaSequenceIds", UNSET))

        aa_sequence_ids = cast(List[str], d.pop("aaSequenceIds", UNSET))

        custom_entity_ids = cast(List[str], d.pop("customEntityIds", UNSET))

        mixture_ids = cast(List[str], d.pop("mixtureIds", UNSET))

        oligo_ids = cast(List[str], d.pop("oligoIds", UNSET))

        projects_archival_change = cls(
            project_ids=project_ids,
            folder_ids=folder_ids,
            entry_ids=entry_ids,
            protocol_ids=protocol_ids,
            dna_sequence_ids=dna_sequence_ids,
            aa_sequence_ids=aa_sequence_ids,
            custom_entity_ids=custom_entity_ids,
            mixture_ids=mixture_ids,
            oligo_ids=oligo_ids,
        )

        return projects_archival_change
