from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.translation_regions_item import TranslationRegionsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="Translation")


@attr.s(auto_attribs=True)
class Translation:
    """  """

    start: Union[Unset, int] = UNSET
    end: Union[Unset, int] = UNSET
    strand: Union[Unset, int] = UNSET
    amino_acids: Union[Unset, str] = UNSET
    regions: Union[Unset, List[TranslationRegionsItem]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        start = self.start
        end = self.end
        strand = self.strand
        amino_acids = self.amino_acids
        regions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.regions, Unset):
            regions = []
            for regions_item_data in self.regions:
                regions_item = regions_item_data.to_dict()

                regions.append(regions_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if strand is not UNSET:
            field_dict["strand"] = strand
        if amino_acids is not UNSET:
            field_dict["aminoAcids"] = amino_acids
        if regions is not UNSET:
            field_dict["regions"] = regions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start = d.pop("start", UNSET)

        end = d.pop("end", UNSET)

        strand = d.pop("strand", UNSET)

        amino_acids = d.pop("aminoAcids", UNSET)

        regions = []
        _regions = d.pop("regions", UNSET)
        for regions_item_data in _regions or []:
            regions_item = TranslationRegionsItem.from_dict(regions_item_data)

            regions.append(regions_item)

        translation = cls(
            start=start,
            end=end,
            strand=strand,
            amino_acids=amino_acids,
            regions=regions,
        )

        return translation
