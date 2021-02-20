from typing import Dict, List, Optional, Type
import logging
import sys
from argparse import ArgumentParser, Namespace, _SubParsersAction
from abc import abstractmethod
from importlib import import_module

from pymdmix_core.settings import SETTINGS
from pymdmix_core.parser import MDMIX_PARSER, get_plugin_subparsers


logger = logging.getLogger(__name__)


class PluginAction:

    ACTION_NAME: str = "action"

    def __init__(self, subparser: _SubParsersAction) -> None:
        self.parser = subparser.add_parser(self.ACTION_NAME, parents=self.get_parents())
        self.init_parser()

    @abstractmethod
    def run(self, args: Namespace) -> None:
        pass

    def init_parser(self):
        pass

    def get_parents(self) -> List[ArgumentParser]:
        return []


class Plugin:

    NAME: str = "plugin"
    HELP_STRING: str = "plugin help"
    LOAD_CONFIG: bool = False
    CONFIG_FILE: str = "pymdmix_core.yml"
    ALLOW_EMPTY_ACTION = False

    def init_parser(self) -> None:
        """
        override this method to configure options for the plugin parser other than actions parsers.
        plugin parser passed as parameter.
        """
        pass

    def init_actions(self, action_subparser):
        """
        Override this method to initialize and register actions associated to this plugin.
        This function will be called on super().__init__
        """
        pass

    def __init__(self, master_parser: ArgumentParser) -> None:
        self.load_config()
        self.actions: Dict[str, PluginAction] = {}
        self.master_parser = master_parser
        subparser = get_plugin_subparsers(self.master_parser)
        self.parser = subparser.add_parser(self.NAME)
        self.init_parser()
        self.action_subparser = self.parser.add_subparsers(dest="action", required=(not self.ALLOW_EMPTY_ACTION))
        self.init_actions(self.action_subparser)

    def register_action(self, action: PluginAction):
        self.actions[action.ACTION_NAME] = action

    def run(self, args: Namespace) -> None:
        action = self.actions.get(args.action)
        if action is None:
            if not self.ALLOW_EMPTY_ACTION:
                self.parser.print_help(sys.stderr)
                raise ValueError("Action is mandatory")
        else:
            action.run(args)

    def load_config(self) -> None:
        if self.LOAD_CONFIG:
            SETTINGS.update_settings_with_file(SETTINGS.get_defaults_filename(self.CONFIG_FILE))


class PluginManager:

    def __init__(self, parser: Optional[ArgumentParser] = None) -> None:
        self.plugins: Dict[str, Plugin] = {}
        self.parser = parser if parser is not None else MDMIX_PARSER

    def load_plugin(self, plugin_name: str):
        mod = import_module(plugin_name)
        plugin_class: Type[Plugin] = mod.get_plugin_class()
        self.plugins[plugin_class.NAME] = plugin_class(self.parser)


MDMIX_PLUGIN_MANAGER = PluginManager()
