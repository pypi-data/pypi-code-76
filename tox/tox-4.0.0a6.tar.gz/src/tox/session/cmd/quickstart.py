import sys
from pathlib import Path
from textwrap import dedent

from packaging.version import Version

from tox.config.cli.parser import ToxParser
from tox.plugin.impl import impl
from tox.session.state import State
from tox.version import __version__


@impl
def tox_add_option(parser: ToxParser) -> None:
    our = parser.add_command(
        "quickstart",
        ["q"],
        "Command-line script to quickly tox config file for a Python project",
        quickstart,
    )
    our.add_argument(
        "quickstart_root",
        metavar="root",
        default=Path().absolute(),
        help="folder to create the tox.ini file",
        type=Path,
    )


def quickstart(state: State) -> int:  # noqa: U100
    root = state.options.quickstart_root.absolute()
    tox_ini = root / "tox.ini"
    if tox_ini.exists():
        print(f"{tox_ini} already exist, refusing to overwrite")
        return 1
    version = str(Version(__version__.split("+")[0]))
    text = f"""
        [tox]
        env_list =
            py{''.join(str(i) for i in sys.version_info[0:2])}
        minversion = {version}

        [testenv]
        description = run the tests with pytest
        package = wheel
        wheel_build_env = .pkg
        deps =
            pytest>=6
        commands =
            pytest {{tty:--color=yes}} {{posargs}}
    """
    content = dedent(text).lstrip()

    print(f"tox {__version__} quickstart utility, will create {tox_ini}:")
    print(content, end="")

    root.mkdir(parents=True, exist_ok=True)
    tox_ini.write_text(content)
    return 0
