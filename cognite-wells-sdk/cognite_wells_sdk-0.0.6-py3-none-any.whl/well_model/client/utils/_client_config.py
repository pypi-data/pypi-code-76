import os
import pprint
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Union

from cognite.well_model.client.utils._token_generator import TokenGenerator
from cognite.well_model.client.utils.exceptions import CogniteAPIKeyError


class Cluster(str, Enum):
    BP = "bp"
    API = "api"
    GREENFIELD = "greenfield"


@dataclass
class _DefaultConfig:
    # Per client
    api_key: Optional[str] = field(init=False, default_factory=lambda: os.getenv("COGNITE_API_KEY"))
    project: str = os.environ["COGNITE_PROJECT"]
    client_name: str = "cognite-wells-client"
    cluster: str = Cluster.API
    base_url: str = "https://well-service-cognitedata-development.cognite.ai"
    max_workers: int = 10
    headers: Dict[str, str] = field(default_factory=dict)
    timeout: int = 30

    # Tokens
    token_client_id: Optional[str] = os.getenv("COGNITE_CLIENT_ID")
    token_client_secret: Optional[str] = os.getenv("COGNITE_CLIENT_SECRET")
    token_url: Optional[str] = os.getenv("COGNITE_TOKEN_URL")
    token_scopes = os.getenv("COGNITE_TOKEN_SCOPES", "").split(",")
    token_custom_args: Dict[str, str] = field(default_factory=dict)

    # Global
    max_retries = 10
    max_retry_backoff = 30
    max_connection_pool_size = 50
    disable_ssl = False


class ClientConfig(_DefaultConfig):
    def __init__(
        self,
        api_key: Optional[str] = None,
        project: Optional[str] = None,
        client_name: Optional[str] = None,
        cluster: Optional[Cluster] = None,
        base_url: Optional[str] = None,
        max_workers: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        token: Optional[Union[Callable[[], str], str]] = None,
        token_url: Optional[str] = None,
        token_client_id: Optional[str] = None,
        token_client_secret: Optional[str] = None,
        token_scopes: Optional[List[str]] = None,
        token_custom_args: Dict[str, str] = field(default_factory=dict),
    ):
        super().__init__()

        self.api_key: Optional[str] = api_key or self.api_key
        self.project: str = project or self.project
        self.cluster: Cluster = cluster or self.cluster
        self.client_name: str = client_name or self.client_name
        self.base_url: str = (base_url or self.base_url).rstrip("/")
        self.max_workers: int = max_workers or self.max_workers
        self.headers: Dict[str, str] = headers or self.headers
        self.timeout: int = timeout or self.timeout

        # Tokens
        self.token = token
        self.token_url = token_url
        self.token_client_id = token_client_id
        self.token_client_secret = token_client_secret
        self.token_scopes = token_scopes  # type: ignore
        self.token_custom_args = token_custom_args

        if self.api_key is None and self.token is None:

            # If no api_key or token is present; try setting up a token generator
            token_generator = TokenGenerator(
                self.token_url,
                self.token_client_id,
                self.token_client_secret,
                self.token_scopes,
                self.token_custom_args,
            )

            # 'True' if all parameters for generating a token is set
            if token_generator.token_params_set():
                # token is a Callable. If token is about to expire or is 'None', a new token will be generated
                self.token = lambda: token_generator.return_access_token()

            if self.token is None:
                raise CogniteAPIKeyError("No API key or Token have been specified")

        if self.client_name is None:
            raise ValueError("No client name has been specified in the Cognite Wells Client")

    def __str__(self):
        """ overloading the printing of the class """
        attr = self.__dict__
        del attr["api_key"]
        return pprint.pformat(attr, indent=4)
