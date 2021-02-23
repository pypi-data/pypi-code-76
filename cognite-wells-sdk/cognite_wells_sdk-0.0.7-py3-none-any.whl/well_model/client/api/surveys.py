import logging
from typing import Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.client.utils._client_config import Cluster
from cognite.well_model.client.utils._deserialize import deserialize_object
from cognite.well_model.model.model.survey import Survey
from cognite.well_model.model.model.survey_data import SurveyData
from cognite.well_model.model.model.survey_data_request import SurveyDataRequest
from cognite.well_model.model.model_utils import model_to_dict

logger = logging.getLogger("WellsAPI")


class SurveysAPI:
    def __init__(self, wells_client: APIClient, project: str, cluster: Cluster):
        self.surveys_client = wells_client
        self.project = project
        self.cluster = cluster

        @extend_class(Survey)
        def data(survey) -> Optional[SurveyData]:
            return self.get_data(data_request=SurveyDataRequest(id=survey.id))

    def _get_path(self, base_url: str):
        return f"/{self.project}{base_url}?env={self.cluster}"

    def get_trajectory(self, wellbore_id: int) -> Optional[Survey]:
        """
        Get trajectory from a cdf asset id

        @param wellbore_id: cdf asset id
        @return: Survey object
        """
        path = self._get_path(f"/wellbores/{wellbore_id}/trajectory")

        response: Response = self.surveys_client.get(path)
        survey = response.json()
        return deserialize_object(survey, Survey)  # type: ignore

    def get_data(self, data_request: SurveyDataRequest) -> Optional[SurveyData]:
        """
        Get data from a survey id and other parameters

        @param data_request: data request object
        @return: SurveyData object
        """
        path = self._get_path("/surveys/data")

        data_request_serialised = model_to_dict(data_request)
        response: Response = self.surveys_client.post(path, data_request_serialised)
        survey_data = response.json()
        return deserialize_object(survey_data, SurveyData)  # type: ignore
