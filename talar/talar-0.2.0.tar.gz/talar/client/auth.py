from requests.auth import AuthBase


class ApiKeyAuth(AuthBase):
    def __init__(self, project_id: str, api_key: str):
        self.project_id = project_id
        self.api_key = api_key

    def __call__(self, r):
        r.headers["X-Api-Key"] = f"{self.project_id}.{self.api_key}"
        return r
