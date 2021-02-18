from getpass import getuser
from os import uname

from sentry_sdk.scope import Scope

from .config import Config


def set_scope_tag_org(scope: Scope) -> None:
    try:
        scope.set_tag("org", Config.get_org())
    except KeyError:
        pass


def set_scope_user(scope: Scope) -> None:
    user = {"username": getuser()}
    try:
        user["email"] = Config.get_email()
    except KeyError:
        pass
    scope.set_user(user)


def set_scope_context_os(scope: Scope) -> None:
    u = uname()
    uname_str = f"{u.sysname} {u.nodename} {u.release} {u.version} {u.machine}"
    scope.set_context(
        "os",
        {
            "name": u.sysname,
            "version": u.release,
            "build": u.version,
            "kernel_version": uname_str,
        },
    )
