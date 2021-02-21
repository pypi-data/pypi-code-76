"""FarmOS Area objects."""

from __future__ import annotations

from typing import Dict, List, Union

from farmos_ext.asset import Asset
from farmos_ext.farmobj import FarmObj


class Area(FarmObj):
    """Area located within a Farm."""

    @property
    def assets(self) -> List[Asset]:
        """Assets assigned to area.

        Returns:
            Union[List[Asset], None]: [description]
        """
        return self.farm.assets(self.key('assets'))

    @property
    def description(self) -> str:
        """Explanation string of the asset.

        This is not escaped for any formatting that is present.

        Returns:
            str: Unformatted string.
        """
        return self.key('description')

    @property
    def flags(self) -> List[str]:
        """Flag items assigned.

        Returns:
            List[str]: Assigned flags by name.
        """
        return self.key('flags')

    @property
    def geofield(self) -> List[Dict]:
        """Location of area in `Well-Known Text` format.

        Returns:
            List[Dict]: Described locations.
        """
        return self.key('geofield')

    @property
    def parent(self) -> List[Area]:
        """Parent Area of this Area.

        Returns:
            List[Area]: Generally a single item but stored as a list.
        """
        return self.farm.areas(self.key('parent'))

    @property
    def parents_all(self) -> List[Area]:
        """All parents.

        Returns:
            List[Area]: List of parents.
        """
        return self.farm.areas(self.key('parents_all'))

    @property
    def tid(self) -> Union[int, None]:
        """Taxonomy ID of item.

        Returns:
            Union[int, None]: Unique ID, none if there is no id but this should
            not occur.
        """
        return self.attr('tid', int)

    @property
    def vocabulary(self) -> Dict:
        """Vocabulary item assigned.

        Returns:
            Dict: Vocabulary item with id and name.
        """
        return self.key('vocabulary')
