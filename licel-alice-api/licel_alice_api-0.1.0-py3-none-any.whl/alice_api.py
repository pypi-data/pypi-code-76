from typing import Union, Type, Tuple, Optional

from .consts import (
    ALICE_KEYCLOAK_URL_PROD,
    ALICE_KEYCLOAK_REALM_PROD,
    ALICE_KEYCLOAK_CLIENT_ID_PROD,
    ALICE_API_URL_PROD,
    ALICE_KEYCLOAK_URL_DEV,
    ALICE_API_URL_DEV,
    ALICE_KEYCLOAK_CLIENT_ID_DEV,
    ALICE_KEYCLOAK_REALM_DEV,
)
from .entities import (
    Incident,
    IncidentShortType,
    PKPIncident,
    CrashIncidentItem,
    EnvCheckIncidentItem,
    TamperIncidentItem,
    PKPIncidentItem,
    IncidentType,
    Project,
    FieldAllowed,
)
from .keycloak_authorized_api import KeycloakAuthorizedAPI
from .params import ListParams
from .responses import ListResponse
from .utils import DictWrapper


class AliceAPI:
    """
    API for Alice - Real-Time Attack Telemetry and Threat Intelligence
    """

    __api: KeycloakAuthorizedAPI

    def __init__(self, username: str, password: str, __dev: bool = False):
        self.__api = KeycloakAuthorizedAPI(
            keycloak_url=(
                ALICE_KEYCLOAK_URL_DEV if __dev is True else ALICE_KEYCLOAK_URL_PROD
            ),
            api_url=(ALICE_API_URL_DEV if __dev is True else ALICE_API_URL_PROD),
            client_id=(
                ALICE_KEYCLOAK_CLIENT_ID_DEV
                if __dev is True
                else ALICE_KEYCLOAK_CLIENT_ID_PROD
            ),
            realm=(
                ALICE_KEYCLOAK_REALM_DEV if __dev is True else ALICE_KEYCLOAK_REALM_PROD
            ),
            username=username,
            password=password,
        )

    def get_incident(
        self, incident_id: int
    ) -> Union[
        PKPIncidentItem, EnvCheckIncidentItem, TamperIncidentItem, CrashIncidentItem
    ]:
        """
        Get one incident by ID
        :param incident_id: ID of incident
        """
        incident = self.__api.get(f"incident/{incident_id}")
        incident_type = IncidentType(incident.get("type"))

        if incident_type == IncidentType.PKP:
            return PKPIncidentItem(incident)
        if incident_type == IncidentType.ENV_CHECK:
            return EnvCheckIncidentItem(incident)
        if incident_type == IncidentType.TAMPER:
            return TamperIncidentItem(incident)
        if incident_type == IncidentType.CRASH:
            return CrashIncidentItem(incident)

    def get_incident_search(
        self, query: str, params: ListParams = ListParams(), project_id: int = None
    ) -> ListResponse[Incident]:
        """
        Search incidents
        :param query: search query, see ListParams docs
        :param params: list parameters
        :param project_id: filter result by project_id
        """
        return ListResponse(
            self.__api.get(
                "incident/search",
                params={
                    **ListParams(sort=params.sort, page=params.page, query=query),
                    "project_id": project_id,
                },
            ),
            Incident,
        )

    def __get_incident_list(
        self,
        incident_type: IncidentShortType,
        wrapper: Type[DictWrapper],
        params: ListParams,
        project_id: int,
    ) -> ListResponse:
        return ListResponse(
            self.__api.get(
                f"{incident_type}", params={**params, "project_id": project_id}
            ),
            wrapper,
        )

    def get_pkp_incident_list(
        self,
        params: ListParams = ListParams(),
        project_id: int = None,
    ) -> ListResponse[PKPIncident]:
        """
        List of PKP incidents
        :param params: list parameters
        :param project_id: filter result by project_id
        """
        return self.__get_incident_list(
            IncidentShortType.PKP, PKPIncident, params, project_id
        )

    def get_tamper_incident_list(
        self,
        params: ListParams = ListParams(),
        project_id: int = None,
    ) -> ListResponse[Incident]:
        """
        List of Tamper incidents
        :param params: list parameters
        :param project_id: filter result by project_id
        """
        return self.__get_incident_list(
            IncidentShortType.TAMPER, Incident, params, project_id
        )

    def get_crash_incident_list(
        self,
        params: ListParams = ListParams(),
        project_id: int = None,
    ) -> ListResponse[Incident]:
        """
        List of Crash incidents
        :param params: list parameters
        :param project_id: filter result by project_id
        """
        return self.__get_incident_list(
            IncidentShortType.CRASH, Incident, params, project_id
        )

    def get_env_check_incident_list(
        self,
        params: ListParams = ListParams(),
        project_id: int = None,
    ) -> ListResponse[Incident]:
        """
        List of Environment Check incidents
        :param params: list parameters
        :param project_id: filter result by project_id
        """
        return self.__get_incident_list(
            IncidentShortType.ENV_CHECK, Incident, params, project_id
        )

    def get_project_list(
        self, params: ListParams = ListParams()
    ) -> ListResponse[Project]:
        """
        List of projects
        :param params: list parameters
        """
        return ListResponse(self.__api.get("projects", params={**params}), Project)

    def get_country_report(
        self,
        from_timestamp: int,
        to_timestamp: int,
        incident_type: IncidentShortType = None,
        project_id: int = None,
    ) -> ListResponse[Tuple[Optional[str], int]]:
        """
        Count incidents by countries
        :param from_timestamp:
        :param to_timestamp:
        :param incident_type: filter result by incident type
        :param project_id: filter result by project_id
        :return:
        """
        return ListResponse(
            self.__api.get(
                "report/countries",
                params={
                    "from": from_timestamp,
                    "to": to_timestamp,
                    "project_id": project_id,
                    "type": incident_type,
                },
            )
        )

    def get_time_report(
        self,
        from_timestamp: int,
        to_timestamp: int,
        interval_sec: int = None,
        incident_type: IncidentShortType = None,
        project_id: int = None,
    ) -> ListResponse[Tuple[int, int]]:
        """
        Count incidents by times
        :param from_timestamp:
        :param to_timestamp:
        :param interval_sec: interval in seconds for slicing data
        :param incident_type: filter result by incident type
        :param project_id: filter result by project_id
        :return:
        """
        return ListResponse(
            self.__api.get(
                "report/incidents",
                params={
                    "from": from_timestamp,
                    "to": to_timestamp,
                    "interval": interval_sec,
                    "project_id": project_id,
                    "type": incident_type,
                },
            )
        )

    def get_search_field_list(
        self, incident_type: IncidentShortType = None, project_id: int = None
    ) -> ListResponse[FieldAllowed]:
        """
        List of fields that can be used in query for incident search
        :param incident_type: filter result by incident type
        :param project_id: filter result by project_id
        """
        return ListResponse(
            self.__api.get(
                f'settings/fields/allowed/{incident_type if incident_type is not None else "all"}',
                params={"project_id": project_id},
            ),
            FieldAllowed,
        )
