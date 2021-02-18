from typing import List

from sym.flow.cli.errors import SymAPIRequestError, UnknownOrgError
from sym.flow.cli.helpers.sym_api_client import BaseSymAPIClient
from sym.flow.cli.models import Organization


class SymAPIService:
    def __init__(self, api_client: BaseSymAPIClient):
        self.api_client = api_client

    def set_access_token(self, access_token: str):
        self.api_client.set_access_token(access_token)

    def get_integration_table_data(self) -> List[List[str]]:
        integration_data, request_id = self.api_client.get_integrations()

        try:
            data = []
            for i in integration_data:
                updated_at = i["updated_at"].strftime("%d %b %Y %I:%M%p")
                data.append([i["slug"], i["type"], updated_at])

            return data
        except KeyError:
            raise SymAPIRequestError(
                "Failed to parse data received from the Sym API", request_id
            )

    def get_organization_from_email(self, email: str) -> Organization:
        try:
            org_data, _ = self.api_client.get_organization_from_email(email)

            return Organization(slug=org_data["slug"], client_id=org_data["client_id"])
        except KeyError:
            raise UnknownOrgError(email)

    def verify_login(self, email: str) -> bool:
        """Verifies Auth0 login was successful and the access token received
        will be respected by the Sym API.

        Returns True if login has been verified.
        """

        status_code, _ = self.api_client.verify_login(email)
        return status_code == 200
