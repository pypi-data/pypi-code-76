from fastapi import FastAPI, Request
from magicapi.config import MagicSettings


class G:
    def __init__(self, app: FastAPI = None, request: Request = None, settings: MagicSettings = None) -> None:
        self._app = app
        self._request = request
        self.tasks = []
        self.settings = settings

    @property
    def app(self) -> FastAPI:
        return self._app

    @app.setter
    def app(self, app: FastAPI) -> None:
        self._app = app

    @property
    def request(self) -> Request:
        return self._request

    @request.setter
    def request(self, request: Request) -> None:
        self._request = request

    @property
    def base_url(self) -> str:
        url = str(self.request.url)
        path = self.request.url.path
        url = url[: url.rindex(path)]
        url = url if self.settings.local else url + f"/{self.settings.stage}"
        return url

    @property
    def url(self) -> str:
        return str(self.request.url)


g = G()
