import typing
from functools import partial
from json import JSONDecodeError
from socket import socket
from types import SimpleNamespace

import httpx
import websockets
from sanic import Sanic  # type: ignore
from sanic.asgi import ASGIApp  # type: ignore
from sanic.exceptions import MethodNotSupported  # type: ignore
from sanic.log import logger  # type: ignore
from sanic.request import Request  # type: ignore
from sanic.response import text  # type: ignore

ASGI_HOST = "mockserver"
ASGI_PORT = 1234
ASGI_BASE_URL = f"http://{ASGI_HOST}:{ASGI_PORT}"
HOST = "127.0.0.1"
PORT = None

Sanic.test_mode = True


class TestingResponse(httpx.Response):
    @property
    def status(self):
        return self.status_code

    @property
    def body(self):
        return self.content

    @property
    def content_type(self):
        return self.headers.get("content-type")

    @property
    def json(self):
        if getattr(self, "_json", None):
            return self._json
        try:
            self._json = super().json()
        except (JSONDecodeError, UnicodeDecodeError):
            self._json = None

        return self._json


class SanicTestClient:
    def __init__(
        self, app: Sanic, port: typing.Optional[int] = PORT, host: str = HOST
    ) -> None:
        """Use port=None to bind to a random port"""
        self.app = app
        self.port = port
        self.host = host
        app.listener("after_server_start")(self._start_test_mode)
        app.listener("before_server_stop")(self._end_test_mode)

    @classmethod
    def _start_test_mode(cls, sanic, *args, **kwargs):
        sanic.test_mode = True

    @classmethod
    def _end_test_mode(cls, sanic, *args, **kwargs):
        sanic.test_mode = False

    def get_new_session(self, **kwargs) -> httpx.AsyncClient:
        return httpx.AsyncClient(verify=False, **kwargs)

    async def _local_request(self, method: str, url: str, *args, **kwargs):
        logger.info(url)
        raw_cookies = kwargs.pop("raw_cookies", None)
        session_kwargs = kwargs.pop("session_kwargs", {})

        if method == "websocket":
            ws_proxy = SimpleNamespace()
            async with websockets.connect(url, *args, **kwargs) as websocket:
                ws_proxy.ws = websocket
                ws_proxy.opened = True
            return ws_proxy
        else:
            async with self.get_new_session(**session_kwargs) as session:

                try:
                    if method == "request":
                        args = tuple([url] + list(args))
                        url = kwargs.pop("http_method", "GET").upper()
                    response = await getattr(session, method.lower())(
                        url, *args, **kwargs
                    )
                except httpx.HTTPError as e:
                    if hasattr(e, "response"):
                        response = getattr(e, "response")
                    else:
                        logger.error(
                            f"{method.upper()} {url} received no response!",
                            exc_info=True,
                        )
                        return None

                response.__class__ = TestingResponse

                if raw_cookies:
                    response.raw_cookies = {}

                    for cookie in response.cookies.jar:
                        response.raw_cookies[cookie.name] = cookie

            return response

    @classmethod
    def _collect_request(cls, results, request):
        if results[0] is None:
            results[0] = request

    async def _collect_response(
        self,
        method,
        url,
        exceptions,
        results,
        sanic,
        loop,
        **request_kwargs,
    ):
        try:
            response = await self._local_request(method, url, **request_kwargs)
            results[-1] = response
            if method == "websocket":
                await response.ws.close()
        except Exception as e:
            logger.exception("Exception")
            exceptions.append(e)
        finally:
            self.app.stop()

    async def _error_handler(self, request, exception):
        if request.method in ["HEAD", "PATCH", "PUT", "DELETE"]:
            return text("", exception.status_code, headers=exception.headers)
        else:
            return self.app.error_handler.default(request, exception)

    def _sanic_endpoint_test(
        self,
        method: str = "get",
        uri: str = "/",
        gather_request: bool = True,
        debug: bool = False,
        server_kwargs: typing.Optional[typing.Dict[str, typing.Any]] = None,
        host: str = None,
        allow_none: bool = False,
        *request_args,
        **request_kwargs,
    ) -> typing.Tuple[
        typing.Optional[Request], typing.Optional[TestingResponse]
    ]:
        results = [None, None]
        exceptions: typing.List[Exception] = []

        server_kwargs = server_kwargs or {"auto_reload": False}
        _collect_request = partial(self._collect_request, results)

        # This is required for the new Sanic router.
        # Once that is merged we can remove this here.
        try:
            self.app.router.reset()
            self.app.router.finalize()
        except AttributeError:
            ...

        if gather_request:
            self.app.request_middleware.appendleft(  # type: ignore
                _collect_request
            )

        self.app.exception(MethodNotSupported)(self._error_handler)

        if self.port:
            server_kwargs = dict(
                host=host or self.host,
                port=self.port,
                **server_kwargs,
            )
            host, port = host or self.host, self.port
        else:
            sock = socket()
            sock.bind((host or self.host, 0))
            server_kwargs = dict(sock=sock, **server_kwargs)
            host, port = sock.getsockname()
            self.port = port

        if uri.startswith(
            ("http:", "https:", "ftp:", "ftps://", "//", "ws:", "wss:")
        ):
            url = uri
        else:
            uri = uri if uri.startswith("/") else f"/{uri}"
            scheme = "ws" if method == "websocket" else "http"
            url = f"{scheme}://{host}:{port}{uri}"
        # Tests construct URLs using PORT = None, which means random port not
        # known until this function is called, so fix that here
        url = url.replace(":None/", f":{port}/")

        self.app.listener("after_server_start")(
            partial(
                self._collect_response,
                method,
                url,
                exceptions,
                results,
                **request_kwargs,
            )
        )

        self.app.run(debug=debug, **server_kwargs)
        self.app.listeners["after_server_start"].pop()

        if exceptions:
            raise ValueError(f"Exception during request: {exceptions}")

        if gather_request:
            try:
                self.app.request_middleware.remove(  # type: ignore
                    _collect_request
                )
            except BaseException:  # noqa
                pass

            try:
                request, response = results
                if response is None:
                    if not allow_none:
                        raise ValueError(
                            "No response returned to Sanic Test Client."
                        )
                return request, response
            except BaseException:  # noqa
                if not allow_none:
                    raise ValueError(
                        "Request and response object expected, "
                        f"got ({results})"
                    )
                return None, None
        else:
            try:
                if results[-1] is None:
                    if not allow_none:
                        raise ValueError(
                            "No response returned to Sanic Test Client."
                        )
                return None, results[-1]
            except BaseException:  # noqa
                if not allow_none:
                    raise ValueError(
                        f"Request object expected, got ({results})"
                    )
                return None, None

    def request(self, *args, **kwargs):
        return self._sanic_endpoint_test("request", *args, **kwargs)

    def get(self, *args, **kwargs):
        return self._sanic_endpoint_test("get", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._sanic_endpoint_test("post", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._sanic_endpoint_test("put", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._sanic_endpoint_test("delete", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._sanic_endpoint_test("patch", *args, **kwargs)

    def options(self, *args, **kwargs):
        return self._sanic_endpoint_test("options", *args, **kwargs)

    def head(self, *args, **kwargs):
        return self._sanic_endpoint_test("head", *args, **kwargs)

    def websocket(self, *args, **kwargs):
        return self._sanic_endpoint_test("websocket", *args, **kwargs)


class TestASGIApp(ASGIApp):
    async def __call__(self):
        await super().__call__()
        return self.request


async def app_call_with_return(self, scope, receive, send):
    asgi_app = await TestASGIApp.create(self, scope, receive, send)
    return await asgi_app()


class SanicASGITestClient(httpx.AsyncClient):
    def __init__(
        self,
        app: Sanic,
        base_url: str = ASGI_BASE_URL,
        suppress_exceptions: bool = False,
    ) -> None:

        app.__class__.__call__ = app_call_with_return  # type: ignore
        app.asgi = True

        self.sanic_app = app

        transport = httpx.ASGITransport(app=app, client=(ASGI_HOST, ASGI_PORT))

        super().__init__(transport=transport, base_url=base_url)

        self.gather_request = True
        self.last_request = None

        app.listener("after_server_start")(self._start_test_mode)
        app.listener("before_server_stop")(self._end_test_mode)

    def _collect_request(self, request):
        if self.gather_request:
            self.last_request = request
        else:
            self.last_request = None

    @classmethod
    def _start_test_mode(cls, sanic, *args, **kwargs):
        sanic.test_mode = True

    @classmethod
    def _end_test_mode(cls, sanic, *args, **kwargs):
        sanic.test_mode = False

    async def request(  # type: ignore
        self, method, url, gather_request=True, *args, **kwargs
    ) -> typing.Tuple[
        typing.Optional[Request], typing.Optional[TestingResponse]
    ]:

        # This is required for the new Sanic router.
        # Once that is merged we can remove this here.
        try:
            self.sanic_app.router.reset()
            self.sanic_app.router.finalize()
        except AttributeError:
            ...

        if not url.startswith(
            ("http:", "https:", "ftp:", "ftps://", "//", "ws:", "wss:")
        ):
            url = url if url.startswith("/") else f"/{url}"
            scheme = "ws" if method == "websocket" else "http"
            url = f"{scheme}://{ASGI_HOST}:{ASGI_PORT}{url}"

        if self._collect_request not in self.sanic_app.request_middleware:
            self.sanic_app.request_middleware.appendleft(  # type: ignore
                self._collect_request
            )

        self.gather_request = gather_request
        response = await super().request(method, url, *args, **kwargs)

        response.__class__ = TestingResponse

        if gather_request:
            return self.last_request, response  # type: ignore
        return None, response  # type: ignore

    @classmethod
    async def _ws_receive(cls):
        return {}

    @classmethod
    async def _ws_send(cls, message):
        pass

    async def websocket(self, uri, subprotocols=None, *args, **kwargs):
        scheme = "ws"
        path = uri
        root_path = f"{scheme}://{ASGI_HOST}:{ASGI_PORT}"

        headers = kwargs.get("headers", {})
        headers.setdefault("connection", "upgrade")
        headers.setdefault("sec-websocket-key", "testserver==")
        headers.setdefault("sec-websocket-version", "13")
        if subprotocols is not None:
            headers.setdefault(
                "sec-websocket-protocol", ", ".join(subprotocols)
            )

        scope = {
            "type": "websocket",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "headers": [map(lambda y: y.encode(), x) for x in headers.items()],
            "scheme": scheme,
            "root_path": root_path,
            "path": path,
            "query_string": b"",
            "subprotocols": subprotocols,
        }

        # This is required for the new Sanic router.
        # Once that is merged we can remove this here.
        try:
            self.sanic_app.router.reset()
            self.sanic_app.router.finalize()
        except AttributeError:
            ...

        await self.sanic_app(scope, self._ws_receive, self._ws_send)

        return None, {"opened": True}

    def __getstate__(self):
        # Cookies cannot be pickled, because they contain a ThreadLock
        try:
            del self._cookies
        except AttributeError:
            pass
        return self.__dict__

    def __setstate__(self, d):
        try:
            del d["_cookies"]
        except LookupError:
            pass
        self.__dict__.update(d)
        # Need to create a new CookieJar when unpickling,
        # because it was killed on Pickle
        self._cookies = httpx.Cookies()
