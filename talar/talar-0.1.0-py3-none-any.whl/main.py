from typing import Optional

from talar.client import Client
from talar.resources.api_keys import ApiKeys
from talar.resources.currency_conversions import CurrencyConversions
from talar.resources.projects import Projects

DEFAULT_API_VERSION = "1"
DEFAULT_API_BASE = "https://api.talar.app"


class Talar:
    def __init__(
        self,
        project_id: str,
        api_key: str,
        api_version: Optional[str] = None,
        api_base: Optional[str] = None,
    ):
        if api_version is None:
            api_version = DEFAULT_API_VERSION
        if api_base is None:
            api_base = DEFAULT_API_BASE
        api_client = Client(project_id, api_key, api_version, api_base)

        self.projects = Projects(project_id, client=api_client)
        self.projects.api_keys = ApiKeys(self.projects)
        self.currency_conversions = CurrencyConversions(client=api_client)
