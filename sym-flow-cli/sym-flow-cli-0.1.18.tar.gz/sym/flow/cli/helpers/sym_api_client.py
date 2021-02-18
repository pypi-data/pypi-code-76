from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from urllib.parse import quote
from uuid import uuid4

import requests
from dateutil.parser import isoparse
from requests.exceptions import SSLError

from sym.flow.cli.errors import (
    NotAuthorizedError,
    SymAPIMissingEntityError,
    SymAPIRequestError,
    SymAPIUnknownError,
)
from sym.flow.cli.helpers.config import Config


class BaseSymAPIClient(ABC):
    @abstractmethod
    def set_access_token(self, access_token: str):
        pass

    @abstractmethod
    def get_integrations(self) -> Tuple[List[dict], str]:
        pass

    @abstractmethod
    def get_organization_from_email(self, email: str) -> Tuple[dict, str]:
        pass

    @abstractmethod
    def verify_login(self, email: str) -> Tuple[int, str]:
        pass


class SymAPIClient(BaseSymAPIClient):
    def __init__(self, url: str):
        self.base_url = url

        try:
            self.access_token = Config.get_access_token()
        except KeyError:
            self.access_token = None

    def set_access_token(self, access_token: str):
        self.access_token = access_token

    def generate_header(self, auth_required: Optional[bool] = True) -> dict:
        if auth_required and not self.access_token:
            raise NotAuthorizedError

        headers = {"X-Sym-Request-ID": str(uuid4())}

        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        return headers

    def validate_response(self, response: requests.Response, request_id: str) -> None:
        if not response.ok:
            for Err in [SymAPIMissingEntityError]:
                if response.status_code in Err.error_codes:
                    raise Err(response_code=response.status_code, request_id=request_id)
            raise SymAPIUnknownError(
                response_code=response.status_code,
                request_id=request_id,
            )

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        validate: Optional[bool] = True,
        auth_required: Optional[bool] = True,
    ) -> Tuple[requests.Response, str]:
        """Perform a GET request to the Sym API.

        Returns a tuple of (Response, Request ID) so the Request ID
        can be logged if any errors occur.
        """

        if params is None:
            params = {}

        headers = self.generate_header(auth_required=auth_required)
        request_id = headers["X-Sym-Request-ID"]

        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}", params=params, headers=headers
            )
        except SSLError as e:
            raise SymAPIUnknownError(response_code=0, request_id=request_id) from e

        if validate:
            self.validate_response(response, request_id)

        return response, request_id

    def get_organization_from_email(self, email: str) -> Tuple[dict, str]:
        """Exchanges the provided email for the corresponding Organization data."""

        response, request_id = self.get(
            f"login/org-check/{quote(email)}",
            auth_required=False,
        )
        return response.json(), request_id

    def verify_login(self, email: str) -> Tuple[int, str]:
        response, request_id = self.get(f"login/verify/{quote(email)}")
        return response.status_code, request_id

    def get_integrations(self) -> Tuple[List[dict], str]:
        """Retrieve all Sym Integrations accessible to the currently
        authenticated user.

        Converts retrieved Integrations' updated_at string to a datetime object
        with the local timezone.

        Returns the list of integration data as well as the Request ID for tracking.
        """

        response, request_id = self.get("integrations/search")
        integrations = []
        try:
            for integration in response.json():
                integration["updated_at"] = isoparse(
                    integration["updated_at"]
                ).astimezone()
                integrations.append(integration)
        except KeyError:
            raise SymAPIRequestError(
                "Not all required data was returned by the Sym API", request_id
            )

        return integrations, request_id

    def get_slack_install_url(self, integration_name: str) -> Tuple[str, str]:
        """Get the URL that starts the Slack App install flow."""

        response, request_id = self.get(
            "install/slack", params={"integration_name": integration_name}
        )
        return response.json()["url"], request_id

    def uninstall_slack(self, integration_name: str) -> str:
        """Make a request to the Sym API to uninstall the Slack App.

        Raises exception from validate_response on failure. Otherwise,
        assume success.
        """

        _, request_id = self.get(
            "uninstall/slack", params={"integration_name": integration_name}
        )
        return request_id
