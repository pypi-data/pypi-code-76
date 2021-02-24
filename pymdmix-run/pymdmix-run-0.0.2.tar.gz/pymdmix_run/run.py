import sys
import logging
import shlex
from argparse import Namespace
from pymdmix_core.plugin.base import Plugin
from pymdmix_core.plugin.base import MDMIX_PLUGIN_MANAGER
from pymdmix_core.parser import MDMIX_PARSER


logger = logging.getLogger(__name__)


class RunPlugin(Plugin):

    NAME = "run"
    HELP_STRING: str = ""
    LOAD_CONFIG: bool = False
    CONFIG_FILE: str = ""
    ALLOW_EMPTY_ACTION = True

    def init_parser(self) -> None:
        super().init_parser()
        self.parser.add_argument("filename", nargs="*")

    def run(self, args: Namespace) -> None:
        if len(args.filename) == 0:
            self.run_file(sys.stdin)
        for filename in args.filename:
            with open(filename, 'r') as file:
                self.run_file(file)

    def run_file(self, file):
        for line in file:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.find("#") == 0:
                continue
            params = shlex.split(line)
            command_args = MDMIX_PARSER.parse_args(params)
            plugin_name = command_args.plugin
            plugin = MDMIX_PLUGIN_MANAGER.plugins.get(plugin_name)
            if plugin is None:
                raise ValueError(f"plugin '{plugin_name}'' not found")
            plugin.run(command_args)
