from requests import Session
from requests.models import Response
from urllib.parse import urljoin


class SessionHandler(Session):
    def __init__(self, base_url:str, key:str, secret:str) -> None:
        super().__init__()
        self._base_url = base_url
        self.auth = (key, secret)
        self.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    
    def request(self, method:str, url:str,
            params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None
    ) -> Response:
        url = urljoin(self._base_url, url)
        return super().request(method, url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)


class EntityClient:
    def __init__(self, uri:str, session:SessionHandler) -> None:
        self._uri = uri
        self._session = session


class NotFoundError(Exception):
    pass

