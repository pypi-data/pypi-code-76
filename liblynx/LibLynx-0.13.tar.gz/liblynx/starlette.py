import logging
import liblynx

from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
    AuthCredentials,
)
from starlette.datastructures import URL
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send

import hmac
import base64


class LibLynxUser(SimpleUser):
    def __init__(self, account_id: str, username: str) -> None:
        self.account_id = str(account_id)
        self.username = username


class LibLynxAuthHTTPMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.connect = liblynx.Connect()

    async def authenticate(self, request):
        llid = request.cookies.get("llid")
        if llid:
            logging.debug("Has cookie %s" % llid)
            try:
                plain_cookie = base64.b64decode(llid.encode("utf8")).decode("utf8")
                cookie_version, llid, ll_accountname, llid_sig = plain_cookie.split(
                    "\n"
                )
                sig = hmac.new(
                    self.connect.client_secret.encode("utf8"),
                    llid.encode("utf8"),
                    digestmod="sha256",
                ).hexdigest()
                logging.debug("sig %s" % sig)
                logging.debug("llid_sig %s" % llid_sig)
                if sig == llid_sig:
                    return (
                        AuthCredentials(["authenticated"]),
                        LibLynxUser(llid, ll_accountname),
                    )
            except:
                logging.debug("Cookie parsing in LibLynxAuthBackend caused exception",)
                raise AuthenticationError("Cookie Parsing failed")

        identification = self.connect.new_identification(
            request.headers.get("X-Forwarded-For", request.client.host),
            str(URL(scope=request.scope)),
            request.headers.get("User-Agent", "<unknown>"),
        )
        logging.debug(
            "identification in LibLynxAuthBackend is %s", identification["id"]
        )

        if identification["status"] == "identified":
            return (
                AuthCredentials(["authenticated"]),
                LibLynxUser(
                    identification["account"].get("publisher_reference")
                    or "brill",  # NOTE how we use the Publisher reference and NOT the account id
                    identification["account"]["account_name"],
                ),
            )
        return  (
                AuthCredentials(["authenticated"]),
                LibLynxUser(
                    "anon",  # NOTE how we use the Publisher reference and NOT the account id
                    "Anonymous",
                ),
            )

        # Disable WAYF temporarily, and make all access Anonymous if not directly identified
        # elif identification["status"] == "wayf":
        #     logging.debug(
        #         "WAYF needed, asking for %s", identification["_links"]["wayf"]["href"]
        #     )
        #     raise WAYFException(identification["_links"]["wayf"]["href"])
        return AuthCredentials(), UnauthenticatedUser()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        try:
            scope["auth"], scope["user"] = await self.authenticate(request)
            response = await self.dispatch_func(request, self.call_next)
        except AuthenticationError as exc:
            if isinstance(exc, WAYFException):
                response = RedirectResponse(url=exc.redirect_to)
            else:
                response = PlainTextResponse(str(exc), status_code=400)
                response.delete_cookie("llid")

        await response(scope, receive, send)

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if not request.cookies.get("llid") and isinstance(request.user, LibLynxUser):
            sig = hmac.new(
                self.connect.client_secret.encode("utf8"),
                request.user.account_id.encode("utf8"),
                digestmod="sha256",
            ).hexdigest()
            logging.debug("signed cookie sig %s" % sig)
            cookie = "2\n%s\n%s\n%s" % (
                request.user.account_id,
                request.user.username,
                sig,
            )
            cookie = base64.b64encode(cookie.encode("utf8")).decode("utf8")
            response.set_cookie(
                "llid", cookie, expires=(60 * 60 * 24 * 7)
            )  # expires in one week
        return response


class WAYFException(AuthenticationError):
    def __init__(self, redirect_to: str = None) -> None:
        self.redirect_to = redirect_to
