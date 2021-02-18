import logging
from typing import Any, Callable, ClassVar, List

from click import Command, Context, Group
from click.exceptions import Abort, ClickException, Exit
from sentry_sdk.api import push_scope

from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.util import is_prod_mode

from ..errors import UnknownError, get_active_env_vars
from ..saml_clients.chooser import choose_saml_client
from . import segment
from .tee import Tee, TeeStdErr, TeeStdOut


class AutoTagCommand(Command):
    """
    A command where each invocation sets the Sentry tag with the
    command's name automatically. Additionally, any CliErrors
    raised from the command are logged.
    """

    def invoke(self, ctx: Context) -> Any:
        segment.track(
            "Command Executed",
            global_options=ctx.find_object(GlobalOptions),
            command=ctx.info_name,
            options=ctx.obj.to_dict(),
        )
        with push_scope() as scope:
            scope.set_tag("command", ctx.info_name)
            scope.set_extra("options", ctx.obj.to_dict())
            return super().invoke(ctx)

    def parse_args(self, ctx, args):
        """
        To work around https://github.com/pallets/click/issues/714, we are doing a trick:
        we always parse a resource *option* from the root command, and then we sometimes
        rewrite the args passed to a child command before parsing the resource *argument*.
        """
        if (
            self.params
            and (resource := ctx.parent.params.get("resource"))
            and self.params[0].name == "resource"
            and (
                not args
                or not choose_saml_client(
                    ctx.parent.params["saml_client_name"]
                ).validate_resource(args[0])
            )
        ):
            args = [resource] + args
        return super().parse_args(ctx, args)

    def format_epilog(self, ctx, formatter):
        if not self.epilog:
            formatter.write(get_active_env_vars())
        super().format_epilog(ctx, formatter)


class SymGroup(Group):
    """
    A group where any defined commands automatically use
    AutoTagCommand.
    """

    tees: ClassVar[List[Tee]] = []
    instances = []

    def __init__(self, *args: Any, **attrs: Any) -> None:
        super().__init__(*args, **attrs)
        SymGroup.instances.append(self)

    def __del__(self):
        self.__class__.reset_tees()

    @classmethod
    def reset_tees(cls):
        for tee in cls.tees:
            tee.close()
        cls.tees = []

    def invoke(self, ctx: Context) -> Any:
        if (log_dir := ctx.params.get("log_dir")) :
            # Don't register exit handler so exceptions are teed.
            # Instead, __del__ will be called when the program exits.
            self.__class__.tees.extend((TeeStdOut(log_dir), TeeStdErr(log_dir)))
            logging_filename = Tee.path_for_fd(log_dir, "logging")
        else:
            logging_filename = None

        if ctx.params.get("debug"):
            logging.basicConfig(level=logging.DEBUG, filename=logging_filename)
            logging.getLogger("segment").setLevel(logging.WARNING)
        else:
            logging.getLogger("segment").setLevel(logging.CRITICAL)

        try:
            return super().invoke(ctx)
        except (ClickException, Abort, Exit):
            raise
        except KeyboardInterrupt:
            pass
        except Exception as e:
            if not is_prod_mode() or ctx.params.get("debug"):
                raise e
            raise UnknownError(e)

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], AutoTagCommand]:
        return super().command(*args, **kwargs, cls=AutoTagCommand)  # type: ignore
