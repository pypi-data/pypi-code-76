import shlex
import subprocess
import sys
import time
from functools import wraps
from subprocess import PIPE, CalledProcessError
from typing import Any, Callable, Iterator, Optional, Sequence, TypeVar, cast

import analytics
import click
from sentry_sdk.api import configure_scope
from sentry_sdk.hub import init as sentry_init

from sym.cli.helpers.util import is_prod_mode

from .errors import (
    CliError,
    ErrorPatterns,
    FailedSubprocessError,
    SuppressedError,
    raise_if_match,
)
from .helpers import segment
from .helpers.config import Config
from .helpers.global_options import GlobalOptions
from .helpers.keywords_to_options import Argument, keywords_to_options
from .helpers.os import has_command
from .helpers.sentry import set_scope_context_os, set_scope_tag_org, set_scope_user
from .helpers.tee import Tee
from .saml_clients.saml_client_factory import SAMLClientFactory

# Typing support for decorators is still in need of a lot of work:
# https://github.com/python/mypy/issues/3157. So the current grossness
# with casts is unavoidable for now.


F = TypeVar("F", bound=Callable[..., Any])


def run_subprocess(
    func: Callable[..., Iterator[Sequence[Argument]]]
) -> Callable[..., Optional[Sequence[Optional[str]]]]:
    @wraps(func)
    def impl(
        *args: Any,
        censor_: bool = False,
        capture_output_: bool = False,
        silence_stderr_: bool = True,
        input_: str = None,
        run_subprocess_options_: Optional[GlobalOptions] = None,
        **kwargs: Any,
    ) -> Optional[Sequence[Optional[str]]]:

        options = run_subprocess_options_
        if not options:
            # Ideally we will never need to access click at this level and
            # will instead always pass in options. This is for backward
            # compatibility as we refactor.
            options = click.get_current_context().find_object(GlobalOptions)

        outputs = []
        tee = bool(options.log_dir) and not censor_

        for command in func(*args, **kwargs):
            command = keywords_to_options(command)
            options.dprint(f"exec: {shlex.join(command)}\n")
            if tee:
                command = Tee.tee_command(options.log_dir, command)
            result = subprocess.run(
                command,
                check=True,
                capture_output=capture_output_,
                input=input_,
                stderr=None if (capture_output_ or not silence_stderr_) else PIPE,
                text=True,
                shell=tee,
                executable="/bin/bash" if tee else None,
            )
            outputs.append(result.stdout)
            if not censor_:
                options.dprint(result.stdout)
        if capture_output_:
            return outputs

    return impl


def intercept_errors(
    patterns: ErrorPatterns = {},
    *,
    quiet: bool = False,
    suppress: bool = False,
) -> Callable[[F], F]:
    def decorate(fn: F) -> F:
        @wraps(fn)
        def wrapped(
            *args: Any,
            quiet_: bool = False,
            suppress_: bool = False,
            intercept_errors_options_: Optional[GlobalOptions] = None,
            **kwargs: Any,
        ) -> Any:

            options = intercept_errors_options_
            if not options:
                # Ideally we will never need to access click at this level and
                # will instead always pass in options. This is for backward
                # compatibility as we refactor.
                options = click.get_current_context().find_object(GlobalOptions)

            try:
                return fn(*args, **kwargs)
            except CalledProcessError as err:
                message = err.stderr or ""
                raise_if_match(patterns, message)
                if not (quiet or quiet_):
                    sys.stderr.write(message)
                else:
                    options.dprint(message)
                if suppress or suppress_:
                    raise SuppressedError(err) from err
                else:
                    raise FailedSubprocessError(err) from err

        return cast(F, wrapped)

    return decorate


def command_require_bins(*bins: str) -> Callable[[F], F]:
    """Decorator to declare that the Click command being defined requires
    specific binaries to run successfully.

    See: https://click.palletsprojects.com/en/7.x/commands/#decorating-commands

    Raises:
        CliError: if any required bin could not be found
    """

    def decorate(fn: F) -> F:
        @click.pass_context
        @wraps(fn)
        def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
            for binary in bins:
                if not has_command(binary):
                    raise CliError(f"Unable to find {binary} in your path!")
            return context.invoke(fn, *args, **kwargs)

        return cast(F, wrapped)

    return decorate


def require_bins(*bins: str) -> Callable[[F], F]:
    """Decorator to declare that the function being defined requires
    specific binaries to run successfully.

    Use this decorator to require bins on functions without Click context.

    Raises:
        CliError: if any required bin could not be found
    """

    def decorate(fn: F) -> F:
        @wraps(fn)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            for binary in bins:
                if not has_command(binary):
                    raise CliError(f"Unable to find {binary} in your path!")
            return fn(*args, **kwargs)

        return wrapped

    return decorate


def require_login(fn: F) -> F:
    @click.pass_context
    @wraps(fn)
    def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
        if not Config.is_logged_in():
            raise CliError("Please run `sym login` first")
        return context.invoke(fn, *args, **kwargs)

    return cast(F, wrapped)


def loses_interactivity(fn: F) -> F:
    @click.pass_context
    @wraps(fn)
    def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
        if (resource := kwargs.get("resource")) :
            saml_client = SAMLClientFactory.create_saml_client(
                resource, context.find_object(GlobalOptions)
            )
            saml_client.ensure_session()
        return context.invoke(fn, *args, **kwargs)

    return cast(F, require_login(wrapped))


def skip_analytics(fn: F) -> F:
    @click.pass_context
    @wraps(fn)
    def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
        options = context.ensure_object(GlobalOptions)
        options.disable_analytics = True
        return context.invoke(fn, *args, **kwargs)

    return cast(F, wrapped)


def setup_segment(**kwargs: Any) -> Callable[[F], F]:
    analytics.default_client = analytics.client.Client(send=is_prod_mode(), **kwargs)

    def decorator(fn: F) -> F:
        @click.pass_context
        @wraps(fn)
        def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
            segment.identify(context.find_object(GlobalOptions))
            return context.invoke(fn, *args, **kwargs)

        return cast(F, wrapped)

    return decorator


def setup_sentry(**kwargs: Any) -> Callable[[F], F]:
    environment = "pypi" if is_prod_mode() and not Config.is_sym() else "development"
    sample_rate = 1.0 if is_prod_mode() else 0.0
    sentry_init(environment=environment, sample_rate=sample_rate, **kwargs)

    def decorator(fn: F) -> F:
        @click.pass_context
        @wraps(fn)
        def wrapped(context: click.Context, *args: Any, **kwargs: Any) -> Any:
            with configure_scope() as scope:
                set_scope_tag_org(scope)
                set_scope_user(scope)
                set_scope_context_os(scope)
                return context.invoke(fn, *args, **kwargs)

        return cast(F, wrapped)

    return decorator


def retry(*exceptions, count: int = 2, delay: int = None, check_ex=lambda _: True):
    def decorator(fn: F) -> F:
        @wraps(fn)
        def wrapped(*args, **kwargs):
            tries = 0
            while tries < count:
                tries += 1
                try:
                    return fn(*args, **kwargs)
                except exceptions as ex:
                    if not check_ex(ex) or tries == count:
                        raise
                    if delay:
                        time.sleep(delay)

        return cast(F, wrapped)

    return decorator
