import logging
import yaml
import json
from argparse import Namespace, ArgumentParser
from typing import Dict, Optional, Type
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from pymdmix_core.plugin.base import PluginAction, _SubParsersAction
from pymdmix_core.orm import BaseModel, SQL_ENGINE

from pymdmix_core.plugin import Plugin

logger = logging.getLogger(__name__)


def parse_file_from_args(args: Namespace) -> Optional[Dict]:
    if args.yaml is not None:
        with open(args.yaml, 'r') as yml_file:
            return yaml.full_load(yml_file)
    elif args.json is not None:
        with open(args.json, 'r') as json_file:
            return json.load(json_file)


class ActionCreate(PluginAction):

    ACTION_NAME = "create"

    def __init__(self, subparser: _SubParsersAction, parent_plugin: 'CRUDPlugin') -> None:
        super().__init__(subparser)
        self.parent_plugin = parent_plugin

    def run(self, args: Namespace) -> None:
        model = self.parent_plugin.factory(args)
        self.parent_plugin.session.commit()
        if model is None:
            logger.critical("Could not create model")
            exit(1)

    def init_parser(self):
        self.parser.add_argument(
            "--yaml", "-y",
            help="A yaml file with all the necessary parameters to create the new item"
        )
        self.parser.add_argument(
            "--json", "-j",
            help="A json file with all the necessary parameters to create the new item"
        )


class ActionRead(PluginAction):

    ACTION_NAME = "info"

    def __init__(self, subparser: _SubParsersAction, parent_plugin: 'CRUDPlugin') -> None:
        super().__init__(subparser)
        self.parent_plugin = parent_plugin

    def init_parser(self):
        super().init_parser()
        self.parser.add_argument("id", nargs="+")

    def run(self, args: Namespace) -> None:
        session = self.parent_plugin.session
        model_class = self.parent_plugin.CLASS
        models = session.query(model_class).filter(model_class.id.in_(args.id)).all()
        for model in models:
            print(model)


# We will disallow this for now.
#
# class ActionUpdate(PluginAction):
#
#     ACTION_NAME = "update"
#
#     def __init__(self, subparser: _SubParsersAction, parent_plugin: 'CRUDPlugin') -> None:
#         super().__init__(subparser)
#         self.parent_plugin = parent_plugin


class ActionDelete(PluginAction):

    ACTION_NAME = "delete"

    def __init__(self, subparser: _SubParsersAction, parent_plugin: 'CRUDPlugin') -> None:
        super().__init__(subparser)
        self.parent_plugin = parent_plugin

    def init_parser(self):
        super().init_parser()
        self.parser.add_argument("id", nargs="+")

    def run(self, args: Namespace) -> None:
        session = self.parent_plugin.session
        model_class = self.parent_plugin.CLASS
        query = session.query(model_class).filter(model_class.id.in_(args.id))
        query.delete(synchronize_session='fetch')
        session.commit()


class ActionList(PluginAction):

    ACTION_NAME = "list"

    def __init__(self, subparser: _SubParsersAction, parent_plugin: 'CRUDPlugin') -> None:
        super().__init__(subparser)
        self.parent_plugin = parent_plugin

    def run(self, _: Namespace) -> None:
        session = self.parent_plugin.session
        model_class = self.parent_plugin.CLASS
        for model in session.query(model_class).all():
            print(model)


class CRUDPlugin(Plugin):

    NAME = "crud_plugin"
    CLASS: Type[BaseModel] = BaseModel

    def factory(self, args: Namespace) -> Optional[BaseModel]:
        """
        A default factory. If a yaml or json file is passed as argument
        It will be parsed into a dictionary and its key-value pairs passed
        as arguments to the CLASS constructor.
        Override this method for a more refined behavior
        """
        fields = parse_file_from_args(args)
        if fields is not None:
            model = self.CLASS(**fields)
            self.session.add(model)
            self.session.commit()
            return model

    def __init__(self, master_parser: ArgumentParser, engine: Optional[Engine] = None) -> None:
        super().__init__(master_parser)
        self.engine = engine if engine is not None else SQL_ENGINE
        self.session = sessionmaker(bind=self.engine)()
        self.CLASS.metadata.create_all(bind=self.engine)

    def init_actions(self, action_subparser):
        self.register_action(ActionCreate(action_subparser, self))
        self.register_action(ActionRead(action_subparser, self))
        # disabled for now
        # self.register_action(ActionUpdate(action_subparser, self))
        self.register_action(ActionDelete(action_subparser, self))
        self.register_action(ActionList(action_subparser, self))
