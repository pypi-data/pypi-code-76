from contextlib import contextmanager
from os import fchmod, get_exec_path, symlink
from pathlib import Path
from typing import Iterator, Optional, TextIO

from sym.cli.helpers.contexts import push_env
from sym.cli.helpers.os import find_command
from sym.cli.tests.helpers.sandbox import Sandbox as SymSandbox

from sym.flow.cli.helpers.config import Config


class Sandbox(SymSandbox):
    @contextmanager
    def push_xdg_config_home(self) -> Iterator[None]:
        """push_xdg_config_home must be redefined in Symflow CLI because the
        base version from Sym CLI reset's its own Config, not Symflow CLI's
        subclassed Config.
        """

        with push_env("XDG_CONFIG_HOME", str(self.path / ".config")):
            Config.reset()
            yield
