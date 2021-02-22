from typing import List, Optional
from argparse import ArgumentParser, Namespace, _SubParsersAction
import logging
import sys
import yaml
from pymdmix_core.plugin.base import Plugin, PluginAction, PluginManager, MDMIX_PLUGIN_MANAGER
from pymdmix_core.settings import SETTINGS
from pymdmix_core.parser import MDMIX_PARSER

logger = logging.getLogger(__name__)


class MDMix:

    def __init__(self, config: Optional[str] = None) -> None:
        if config is not None:
            SETTINGS.update_settings_with_file(config)

        self.plugin_manager = MDMIX_PLUGIN_MANAGER
        for plugin in SETTINGS["pymdmix_core"]["installed_plugins"]:
            logger.info(f"loading plugin: {plugin}")
            self.plugin_manager.load_plugin(plugin)

    def run(self) -> None:
        args = MDMIX_PARSER.parse_args()
        plugin = self.plugin_manager.plugins.get(args.plugin)
        if plugin is None:
            MDMIX_PARSER.print_help(sys.stderr)
            return

        plugin.run(args)


class ActionList(PluginAction):

    ACTION_NAME = "list"

    def run(self, args: Namespace) -> None:
        print("Available plugins:")
        for plugin_name in MDMIX_PLUGIN_MANAGER.plugins:
            print(f"\t- {plugin_name}")


class ActionLoad(PluginAction):

    ACTION_NAME = "load"

    def __init__(self, subparser: _SubParsersAction, plugin_manager: PluginManager) -> None:
        super().__init__(subparser)
        self.plugin_manager = plugin_manager

    def init_parser(self):
        self.parser.add_argument("plugin_module")

    def run(self, args: Namespace) -> None:
        try:
            self.plugin_manager.load_plugin(args.plugin_module)
        except Exception as e:
            logger.error(f"Unable to load plugin module {args.plugin_module}: {repr(e)}")
            raise e


class ActionAdd(ActionLoad):

    ACTION_NAME = "add"

    def run(self, args: Namespace) -> None:
        try:
            super().run(args)
            defaults_file = SETTINGS.defaults_filename
            defaults = {}
            with open(defaults_file, 'r') as input_defaults_file:
                defaults = yaml.full_load(input_defaults_file)
            installed = defaults["pymdmix_core"]["installed_plugins"]
            if args.plugin_module not in installed:
                installed.append(args.plugin_module)
            with open(defaults_file, 'w') as output_defaults_file:
                yaml.dump(defaults, output_defaults_file)
        except Exception as e:
            logger.error(f"Unable to add plugin module {args.plugin_module} to installed plugins: {repr(e)}")
            raise e


class ActionRemove(ActionLoad):

    ACTION_NAME = "remove"

    def run(self, args: Namespace) -> None:
        try:
            if args.plugin_module is None:
                self.parser.print_help(sys.stderr)
                raise Exception("no plugin module provided")
            defaults_file = SETTINGS.defaults_filename
            defaults = {}
            with open(defaults_file, 'r') as input_defaults_file:
                defaults = yaml.full_load(input_defaults_file)
            installed: List = defaults["pymdmix_core"]["installed_plugins"]
            if args.plugin_module not in installed:
                raise Exception("Not found")
            installed.remove(args.plugin_module)
            with open(defaults_file, 'w') as output_defaults_file:
                yaml.dump(defaults, output_defaults_file)
        except Exception as e:
            logger.error(f"Unable to remove plugin module {args.plugin_module}: {repr(e)}")
            raise e


class CorePlugin(Plugin):

    NAME = "plugin"

    def __init__(self, master_parser: ArgumentParser, plugin_manager: Optional[PluginManager] = None) -> None:
        self.plugin_manager = plugin_manager if plugin_manager is not None else MDMIX_PLUGIN_MANAGER
        super().__init__(master_parser)

    def init_actions(self, action_subparser):
        self.register_action(ActionList(action_subparser))
        self.register_action(ActionLoad(action_subparser, self.plugin_manager))
        self.register_action(ActionAdd(action_subparser, self.plugin_manager))
        self.register_action(ActionRemove(action_subparser, self.plugin_manager))
