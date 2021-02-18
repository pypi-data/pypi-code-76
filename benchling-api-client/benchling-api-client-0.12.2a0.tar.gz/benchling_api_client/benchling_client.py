import base64
from typing import Dict

from benchling_api_client.client import AuthenticatedClient


class BenchlingApiClient(AuthenticatedClient):
    def get_headers(self) -> Dict[str, str]:
        """ Get headers to be used in authenticated endpoints """
        token_encoded = base64.b64encode(f"{self.token}:".encode())
        return {"Authorization": f"Basic {token_encoded.decode()}"}
