from typing import Optional

from requests import Session, codes

from talar.client.auth import ApiKeyAuth
from talar.version import version

try:
    from typing import Literal
except ImportError:
    # Python 3.6 and 3.7 compatibility
    from typing_extensions import Literal

HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]


class Client:
    def __init__(
        self,
        project_id: str,
        api_key: str,
        api_version: str,
        api_base: str,
    ):

        self.project_id = project_id
        self.base_url = f"{api_base}/v{api_version}"

        self.session = Session()
        self.session.auth = ApiKeyAuth(project_id, api_key)
        self.session.headers.update(
            {
                "User-Agent": "Talar Python SDK v{}".format(version),
            }
        )

    def _get_absolute_url(self, path):
        return f"{self.base_url}/{path}"

    def request(
        self,
        method: HttpMethod,
        path: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Optional[dict]:
        response = self.session.request(
            method=method,
            url=self._get_absolute_url(path),
            data=data,
            params=params,
        )
        response.raise_for_status()
        if response.status_code == codes.no_content:
            return None
        return response.json()

    def get(self, path: str, params: Optional[dict] = None) -> dict:
        return self.request("GET", path, params=params)

    def post(self, path: str, data: Optional[dict] = None) -> dict:
        return self.request("POST", path, data=data)

    def put(self, path: str, data: Optional[dict] = None) -> dict:
        return self.request("PUT", path, data=data)

    def delete(self, path: str) -> None:
        self.request("DELETE", path)
