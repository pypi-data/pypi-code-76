import os
import shutil
from argparse import Namespace
from sqlalchemy import Column, String
from pymdmix_core.orm import BaseModel
from pymdmix_core.plugin.crud import CRUDPlugin, ActionCreate, ActionDelete, parse_file_from_args


class ActionCreateProject(ActionCreate):

    def init_parser(self):
        super().init_parser()
        self.parser.add_argument("--name", "-n")
        self.parser.add_argument("--path", "-p")
        self.parser.add_argument("--description", "-d")


class ActionDeleteProject(ActionDelete):

    def init_parser(self):
        super().init_parser()
        self.parser.add_argument("--remove-data", action="store_true")

    def run(self, args: Namespace) -> None:
        if args.remove_data:
            session = self.parent_plugin.session
            model_class: Project = self.parent_plugin.CLASS
            query = session.query(model_class).filter(model_class.id.in_(args.id))
            for target in query.all():
                shutil.rmtree(target.path)
        super().run(args)


class Project(BaseModel):
    __tablename__ = "projects"
    id = Column(String(128), unique=True, primary_key=True)
    description = Column(String(1024))
    path = Column(String(256))

    def __str__(self):
        return f"{self.id} @ {self.path}"

    def __repr__(self):
        return f"Project: {self.id} @ {self.path}\n\t{self.description}"


class ProjectPlugin(CRUDPlugin):

    NAME = "project"
    CLASS = Project

    def factory(self, args: Namespace) -> Project:

        fields = {
            "id": args.name,
            "path": args.path if args.path is not None else os.path.join(os.getcwd(), args.name),
            "description": args.description
        } if args.name is not None else parse_file_from_args(args)

        if fields is not None:
            fields["description"] = args.description if fields.get("description") is None else fields["description"]
            fields["path"] = os.path.abspath(fields["path"])
            os.makedirs(fields["path"], exist_ok=True)
            model = self.CLASS(**fields)
            self.session.add(model)
            self.session.commit()
            return model

    def init_actions(self, action_subparser):
        super().init_actions(action_subparser)
        self.register_action(ActionCreateProject(action_subparser, self))
        self.register_action(ActionDeleteProject(action_subparser, self))
