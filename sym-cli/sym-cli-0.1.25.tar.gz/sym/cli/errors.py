import shlex
import sys
from subprocess import CalledProcessError
from typing import Mapping, Pattern, Sequence, Type, Union

import click
from click import Argument, BadParameter, ClickException, Option
from sentry_sdk import capture_exception, push_scope

from sym.cli.helpers.keywords_to_options import keywords_to_options
from sym.cli.helpers.util import get_param

from .helpers.envvar_option import get_used

ErrorPatterns = Mapping[Pattern[str], Type[Exception]]


def raise_if_match(patterns: ErrorPatterns, msg: str):
    if error := next((err for pat, err in patterns.items() if pat.search(msg)), None):
        raise error


def get_active_env_vars():
    if used := get_used():
        mapping = "\n".join([f"{k}\t--{n}={v}" for k, (n, v) in used.items()])
        envvars = "\n".join(["Active Env Vars:", mapping])
        return f"\n\n{envvars}"
    else:
        return ""


def _format_message(self, file=None):
    msg = click.style(self.message, fg="red", bold=True)
    if hasattr(self, "hints"):
        styled = [click.style(hint, fg="cyan", bold=True) for hint in self.hints]
        hint = "\n\n" + "\n\n".join([f"Hint: {hint}" for hint in styled])
    else:
        hint = ""
    return f"{msg}{hint}{get_active_env_vars()}"


BadParameter.format_message = _format_message


class CliErrorMeta(type):
    _exit_code_count = 2

    def __new__(cls, name, bases, attrs):
        cls._exit_code_count += 1
        klass = super().__new__(cls, name, bases, attrs)
        klass.exit_code = cls._exit_code_count
        return klass


class CliError(ClickException, metaclass=CliErrorMeta):
    def __init__(self, *args, report=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.report = report

    def show(self):
        if self.report:
            with push_scope() as scope:
                scope.level = "info"
                capture_exception()
        super().show()

    def format_message(self):
        return _format_message(self)


class CliErrorWithHint(CliError):
    def __init__(self, message, hints, **kwargs) -> None:
        self.hints = hints if isinstance(hints, list) else [hints]
        super().__init__(message, **kwargs)

    def __str__(self):
        return "\n\n".join(
            [
                self.message,
                *[f"Hint: {hint}" for hint in self.hints],
            ]
        )


class UnavailableResourceError(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "You don't have permission to access the Sym resource you requested.",
            "Request approval and then try again.",
        )


class ResourceNotSetup(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "The Sym resource you requested is not set up properly.",
            "Contact your Sym administrator.",
            report=True,
        )


class TargetNotConnected(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "The instance you tried to SSH into is not connected to AWS Session Manager.",
            "Ask your Sym administrator if they've set up Session Manager.",
        )


class AccessDenied(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "You don't have access to connect to this instance.",
            "Have you requested access?",
        )


class InstanceNotFound(CliError):
    def __init__(self, instance) -> None:
        super().__init__(f"Could not find instance {instance}")


class SAMLClientNotFound(CliError):
    def __init__(self) -> None:
        super().__init__(
            "No valid SAML client found in PATH. Supported clients are listed in `sym --help`."
        )


class OfflineError(CliError):
    def __init__(self) -> None:
        super().__init__("You are currently offline.")


class BotoError(CliErrorWithHint):
    def __init__(self, wrapped: "ClientError", hint: str) -> None:
        message = f"An AWS error occured!\n{str(wrapped)}"
        super().__init__(message, hint)


class FailedSubprocessError(CliError):
    def __init__(self, wrapped: Union[CalledProcessError, str]):
        if isinstance(wrapped, str):
            super().__init__(wrapped)
        elif wrapped.stderr:
            super().__init__(
                "\n".join(
                    [
                        f"Cannot run {shlex.join(wrapped.cmd)}.",
                        "\nThe original error was:",
                        wrapped.stderr,
                    ]
                )
            )
        else:
            super().__init__(f"Cannot run {shlex.join(wrapped.cmd)}.")


class SuppressedError(FailedSubprocessError):
    def __init__(self, wrapped: CalledProcessError, echo=False):
        if echo:
            print(wrapped.stderr, file=sys.stderr)
        wrapped.stderr = None
        wrapped.cmd = [wrapped.cmd[0]]
        super().__init__(wrapped)

    def show(self):
        pass


class WrappedSubprocessError(FailedSubprocessError):
    def __init__(self, wrapped, hint, **kwargs) -> None:
        super().__init__(wrapped)
        messages = [
            f"Cannot run {wrapped.cmd[0]} [{wrapped.returncode}]",
            f"Hint: {hint}",
            f"\nThe original error was:",
            wrapped.stderr,
        ]
        CliError.__init__(self, "\n".join(messages), **kwargs)


class MissingPublicKey(WrappedSubprocessError):
    def __init__(self, wrapped, user) -> None:
        super().__init__(wrapped, f"Does the user ({user}) exist on the instance?")


class SamlClientNotSetup(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "Your SAML client is not set up.",
            "Consult the docs for your client.",
        )


class ExpiredCredentials(CliErrorWithHint):
    def __init__(self) -> None:
        super().__init__(
            "Your AWS credentials have expired.",
            "\n".join(
                [
                    "Try running `sym write-creds` again, or run your command with SYM_SESSION_LENGTH=60.",
                    "For more details, see: https://docs.symops.com/docs/common-issues-sym-cli#error-your-aws-credentials-have-expired",
                ]
            ),
        )


class MissingResource(CliErrorWithHint, BadParameter):
    def __init__(
        self,
        profiles: Sequence[str],
        resource_name="resource",
    ) -> None:
        super().__init__(
            "You must supply a resource!",
            self.__class__.gen_hint(resource_name, profiles),
        )

    @classmethod
    def gen_hint(cls, resource_name, profiles) -> str:
        return "\n".join(
            [
                click.style(
                    f"These are the {resource_name}s available to you:",
                    fg="white",
                    reset=False,
                ),
                *[f"  - {key}" for key in profiles],
            ]
        )


class InvalidResource(CliErrorWithHint, BadParameter, KeyError):
    def __init__(
        self,
        resource: str,
        profiles: Sequence[str],
        resource_name="resource",
    ) -> None:
        super().__init__(
            f"Invalid {resource_name} name '{resource}'",
            self.gen_hints(resource, resource_name, profiles),
        )

    def gen_hints(self, resource, resource_name, profiles) -> Sequence[str]:
        hints = [
            "\n".join(
                [
                    f"Has your Sym Implementer set up {resource} yet?",
                    MissingResource.gen_hint(resource_name, profiles),
                ]
            )
        ]
        if (ctx := click.get_current_context()) :
            if ctx.command.params[0].name == resource_name:
                args = [
                    v
                    for k, v in ctx.params.items()
                    if isinstance(get_param(ctx.command, k), Argument)
                ]
                if len(args) == 1:
                    return hints
                opts = {
                    k: v
                    for k, v in ctx.params.items()
                    if isinstance(get_param(ctx.command, k), Option)
                    and get_param(ctx.command, k).get_default(ctx) != v
                }
                cmd = " ".join(
                    [
                        *keywords_to_options([opts]),
                        (
                            click.style(profiles[0], fg="magenta", reset=False)
                            + click.style("", fg="white", reset=False)
                        ),
                        *keywords_to_options(args),
                        *ctx.args,
                    ]
                )
                hints.insert(
                    0,
                    "\n".join(
                        [
                            "Did you forget to pass a RESOURCE as the first argument?",
                            click.style(
                                f"e.g. `{ctx.command_path} {cmd}`",
                                fg="white",
                            ),
                        ]
                    ),
                )

        return hints


class UnknownError(CliErrorWithHint):
    def __init__(self, wrapped: Exception) -> None:
        super().__init__("An unknown error occurred", str(wrapped), report=True)
