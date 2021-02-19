import logging
import urllib.parse
from typing import Dict, List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.wellbores import WellboresAPI
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.client.utils._client_config import Cluster
from cognite.well_model.client.utils._deserialize import deserialize_object
from cognite.well_model.model.model.well import Well
from cognite.well_model.model.model.well_filter import WellFilter
from cognite.well_model.model.model.well_items import WellItems
from cognite.well_model.model.model.wellbore import Wellbore
from cognite.well_model.model.model_utils import model_to_dict

logger = logging.getLogger("WellsAPI")


class WellsAPI:
    def __init__(self, wells_client: APIClient, wellbores_api: WellboresAPI, project: str, cluster: Cluster):
        self.wells_client = wells_client
        self.wellbores_api = wellbores_api
        self.project = project
        self.cluster = cluster

        # wrap all wells with a lazy method
        @extend_class(Well)
        def wellbores(well) -> Optional[List[Wellbore]]:
            return self.wellbores_api.get_from_well(well_id=well.id)

    @staticmethod
    def deserialize_well_items(well_items_dict: Dict) -> WellItems:
        """
        deserialize a json dictionary to a WellItems object

        @param well_items_dict: key-word arguments to deserialize
        @return: List of wells
        """

        # if we set next_cursor=None then you can no longer access it as an attribute of WellItems
        # a solution is to init next_cursor as an empty string
        well_items: WellItems = WellItems(items=[], next_cursor="")
        try:
            items: List[Dict[str, str]] = well_items_dict.get("items", [])
            next_cursor: str = well_items_dict.get("nextCursor", None)

            if next_cursor is not None:
                well_items.next_cursor = next_cursor  # type: ignore
            for item in items:
                well: Optional[Well] = deserialize_object(item, Well)
                if well is not None:
                    well_items.items.append(well)
        except Exception as e:
            logger.info(f"Could not parse well items due to: {e}")

        return well_items

    def _get_path(self, base_url: str):
        return f"/{self.project}{base_url}?env={self.cluster}"

    def _get_label_prefix(self, prefix: str) -> List[str]:
        """
        list valid values for prefix

        @param prefix: which label to filter on
        @return: list of valid label values
        """
        path: str = self._get_path(f"/wells/{prefix}")
        response: Response = self.wells_client.get(url_path=path)
        data: List[str] = response.json()
        return data

    def blocks(self) -> List[str]:
        """ List valid block values """
        return self._get_label_prefix("blocks")

    def fields(self) -> List[str]:
        """ List valid field values """
        return self._get_label_prefix("fields")

    def operators(self) -> List[str]:
        """ List valid operator values """
        return self._get_label_prefix("operators")

    def quadrants(self) -> List[str]:
        """ List valid quadrant values """
        return self._get_label_prefix("quadrants")

    def sources(self) -> List[str]:
        """ List valid source values """
        return self._get_label_prefix("sources")

    def measurements(self) -> List[str]:
        """ List valid measurement type values """
        return self._get_label_prefix("measurements")

    def get_by_id(self, well_id: int) -> Optional[Well]:
        """
        Get well from a cdf asset id

        @param well_id: cdf asset id
        @return: Well object
        """
        path: str = self._get_path(f"/wells/{well_id}")
        response: Response = self.wells_client.get(url_path=path)
        well_data = response.json()
        return deserialize_object(well_data, Well)  # type: ignore

    def list(self, cursor: Optional[str] = None) -> WellItems:
        """
        list all wells

        @param cursor: cursor for pagination
        @return: WellItems object
        """
        path: str = self._get_path("/wells")
        if cursor:
            path += urllib.parse.urlencode({"cursor": f"{cursor}"})
        response: Response = self.wells_client.get(url_path=path)
        well_items = response.json()
        return self.deserialize_well_items(well_items)

    def filter(self, wellFilter: WellFilter, cursor: Optional[str] = None) -> WellItems:
        """
        Get wells that matches the filter

        @param wellFilter: the applied filter
        @param cursor: cursor for paginating results
        @return: WellItems object
        """
        path: str = self._get_path("/wells/list")
        if cursor:
            path += urllib.parse.urlencode({"cursor": f"{cursor}"})
        well_serialized = model_to_dict(wellFilter, serialize=True)
        response: Response = self.wells_client.post(url_path=path, json=well_serialized)
        well_items_data = response.json()
        return self.deserialize_well_items(well_items_data)
