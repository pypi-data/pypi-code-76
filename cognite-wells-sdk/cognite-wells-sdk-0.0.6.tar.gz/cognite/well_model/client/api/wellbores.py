import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.surveys import SurveysAPI
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.client.utils._client_config import Cluster
from cognite.well_model.client.utils._deserialize import deserialize_list, deserialize_object
from cognite.well_model.client.utils.enums import MeasurementType
from cognite.well_model.model.model.asset import Asset
from cognite.well_model.model.model.measurement import Measurement
from cognite.well_model.model.model.survey import Survey
from cognite.well_model.model.model.well_ids import WellIds
from cognite.well_model.model.model.wellbore import Wellbore
from cognite.well_model.model.model_utils import model_to_dict

logger = logging.getLogger("WellboresAPI")


class WellboresAPI:
    def __init__(self, wells_client: APIClient, survey_api: SurveysAPI, project: str, cluster: Cluster):
        self.wells_client = wells_client
        self.survey_api = survey_api
        self.project = project
        self.cluster = cluster

        # wrap all wellbores with a lazy method
        @extend_class(Wellbore)
        def trajectory(wellbore) -> Optional[Survey]:
            return survey_api.get_trajectory(wellbore.id)

        @extend_class(Wellbore)
        def source_assets(wellbore, source_label: Optional[str] = None) -> Optional[List[Asset]]:
            return self.get_sources(wellbore_id=wellbore.id, source_label=source_label)

    def _get_path(self, base_url: str):
        return f"/{self.project}{base_url}?env={self.cluster}"

    def get_by_id(self, wellbore_id: int) -> Optional[Wellbore]:
        """
        Get wellbore from a cdf asset id

        @param wellbore_id: cdf asset id
        @return: Wellbore object
        """
        path: str = self._get_path(f"/wellbores/{wellbore_id}")
        response: Response = self.wells_client.get(url_path=path)
        well_data = response.json()
        return deserialize_object(well_data, Wellbore)  # type: ignore

    def get_from_well(self, well_id: int) -> Optional[List[Wellbore]]:
        """
        get wellbores from a well id

        @param well_id: well id of interest
        @return: wellbores that has the well of interest as parent
        """
        path: str = self._get_path(f"/wells/{well_id}/wellbores")
        response: Response = self.wells_client.get(url_path=path)
        wellbores_data = response.json()
        return deserialize_list(wellbores_data, Wellbore)

    def get_from_wells(self, well_ids: List[int]) -> Optional[List[Wellbore]]:
        """
        Return multiple wellbores from multiple input well ids

        @param well_ids: list of well ids we want the wellbores from
        @return: list of wellbores
        """
        path: str = self._get_path("/wellbores/bywellids")
        ids = WellIds(items=well_ids)
        well_ids_serialized = model_to_dict(ids, serialize=True)
        response: Response = self.wells_client.post(url_path=path, json=well_ids_serialized)
        wellbores_data = response.json()
        return deserialize_list(wellbores_data, Wellbore)

    def get_measurement(self, wellbore_id: int, measurement_type: MeasurementType) -> Optional[List[Measurement]]:
        """
        retrieve measurements for a wellbore

        @param wellbore_id: The wellbore id of interest
        @param measurement_type: The measurement type of interest
        @return: list of measurements
        """
        path: str = self._get_path(f"/wellbores/{wellbore_id}/measurements/{measurement_type}")
        response: Response = self.wells_client.get(url_path=path)
        measurements_data = response.json()
        return deserialize_list(measurements_data["items"], Measurement)

    def get_sources(self, wellbore_id: int, source_label: Optional[str] = None) -> Optional[List[Asset]]:
        """
        Return all source assets associated to a wellbore

        @param wellbore_id: The wellbore id of interest
        @param source_label: the source label for the wellbore object
        @return: list of assets
        """
        path: str = f"/wellbores/{wellbore_id}/sources"
        if source_label is not None:
            path += f"/{source_label}"
        path = self._get_path(path)
        response: Response = self.wells_client.get(url_path=path)
        assets_data = response.json()
        assets = deserialize_list(assets_data, Asset)
        return assets
