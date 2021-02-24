"""Main program."""

import collections
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Sequence

import click

grace_root = Path(__file__).parent


class OrderedGroup(click.Group):
    """Group preserving the order of subcommands."""

    # See: https://stackoverflow.com/a/58323807

    def __init__(
        self,
        name: Optional[str] = None,
        commands: Optional[Dict[str, click.Command]] = None,
        **attrs: Dict[str, Any],
    ) -> None:
        """Construct a group."""
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx: click.Context) -> Dict[str, click.Command]:
        """Return a list of subcommands in the order they should appear."""
        return self.commands


@click.group(cls=OrderedGroup, context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:  # noqa: D103  # to suppress the help message
    pass


@main.command(no_args_is_help=True)
@click.argument("name")
def template(name: str) -> None:
    """Copy a template in.prc to the current directory."""
    src = grace_root / "lib" / "templates" / name / "in.prc"
    dest = Path("in.prc")
    shutil.copy(src, dest)


def _add_template_help() -> None:
    if not template.help:
        return

    template_dir = grace_root / "lib" / "templates"
    names = [str(f.relative_to(template_dir)) for f in template_dir.glob("*/*")]

    if names:
        s = ", ".join(names)
        template.help += f"\n\nNAME must be one of: {s}."


_add_template_help()


def _add_raw_commands() -> None:
    raw_commands = (
        "gracefig",
        "grc",
        "grccut",
        "grcdraw",
        "grcfort",
        "grcmdl",
        "grcmom",
        "grcplot",
        "grcprc",
        "qcdcut",
        "tread",
    )

    args = click.Argument(["args"], required=False, nargs=-1)
    context_settings = {"ignore_unknown_options": True, "help_option_names": []}

    def get_callback(name: str) -> Callable[..., None]:
        # Return a closure that remembers the given name.
        def callback(args: Sequence[str]) -> None:
            invoke_raw_command(name, args)

        return callback

    for name in raw_commands:
        cmd = click.Command(
            name,
            context_settings=context_settings,
            callback=get_callback(name),
            params=[args],
            help=f"Run {name}.",
        )
        main.add_command(cmd)


_add_raw_commands()


def is_raw_command_available(cmd: str) -> bool:
    """Return `True` if the given raw command is actually available."""
    return (grace_root / "bin" / cmd).is_file()


def invoke_raw_command(cmd: str, args: Sequence[str]) -> None:
    """Invoke the given raw command."""
    cmd_args = (str(grace_root / "bin" / cmd),) + tuple(args)

    # We need to give the environment variables GRCMODEL and KINEMPATH.

    model_path = grace_root / "lib" / "model"
    kinem_path = grace_root / "lib" / "dbkinem"

    env = os.environ.copy()
    env["GRCMODEL"] = f".:{model_path}"
    env["KINEMPATH"] = f".:{kinem_path}"

    subprocess.run(cmd_args, check=True, env=env)  # noqa: S603

    if cmd == "grcfort":
        patch_makefile()


def patch_makefile() -> None:
    """Patch Makefile."""
    makefile = Path("Makefile")
    lines = makefile.read_text().splitlines()

    # We need to provide GRACEROOT.

    if any(re.match(r"^\s*GRACEROOT\s*=", line) for line in lines):
        return

    for i, line in enumerate(lines):
        # Insert a line just before GRACEDIR.
        if re.match(r"^\s*GRACEDIR\s*=", line):
            lines.insert(i, f"GRACEROOT = {str(grace_root)}")
            break
    else:
        raise RuntimeError("failed to patch Makefile")

    makefile.write_text("\n".join(lines) + "\n")
