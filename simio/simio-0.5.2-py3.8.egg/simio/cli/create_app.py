import os
from typing import Dict
from string import Template

import click


class ProjectFile:
    """
    Class that contains path for file
    """

    def __init__(self, path: str):
        self.path = os.path.join(os.path.dirname(__file__), path)


PROJECT_STRUCTURE = {
    # fmt: off
    # pylint: disable=line-too-long
    # Default project structure to create
    "{project_name}": {
        "__init__.py": ProjectFile(path=os.path.join("files", "module_init.sim")),
        "mock_client.py": ProjectFile(path=os.path.join("files", "client.sim")),
        "config.py": ProjectFile(path=os.path.join("files", "cfg.sim")),
        "handlers": {
            "__init__.py": ProjectFile(path=os.path.join("files", "module_init.sim")),
            "example_handler.py": ProjectFile(path=os.path.join("files", "example_handler.sim")),
        },
        "workers": {
            "__init__.py": ProjectFile(path=os.path.join("files", "module_init.sim")),
            "ping.py": ProjectFile(path=os.path.join("files", "ping.sim")),
        },
        "crons": {
            "__init__.py": ProjectFile(path=os.path.join("files", "module_init.sim")),
            "heartbeat.py": ProjectFile(path=os.path.join("files", "heartbeat_cron.sim")),
        }
    },
    "tests": {
        "__init__.py": ProjectFile(path=os.path.join("files", "module_init.sim")),
    },
    "run.py": ProjectFile(path=os.path.join("files", "run.sim")),
    "requirements.txt": ProjectFile(path=os.path.join("files", "requirements.sim")),
    "requirements-dev.txt": ProjectFile(path=os.path.join("files", "requirements-dev.sim")),
    "Makefile": ProjectFile(path=os.path.join("files", "local_makefile.sim")),
    "pylintrc": ProjectFile(path=os.path.join("files", "local_pylintrc.sim")),
    # pylint: enable=line-too-long
    # fmt: on
}


@click.command(context_settings={"allow_extra_args": True})
@click.option("--name", prompt="Your project name")
def create_project(name: str):
    """
    CLI for project template generation
    :param name: name of project
    """
    kwargs_container = {"project_name": name}
    _create_project_files(PROJECT_STRUCTURE, os.getcwd(), kwargs_container)


def _read_file_template(path: str, kwargs_container: dict):
    """
    Read data from file and format it with kwargs_container

    :param path: path to file
    :param kwargs_container: kwargs for str format
    :return: formatted file content
    """
    with open(path, "r") as f:
        template = Template(f.read())
        return template.substitute(**kwargs_container)


def _write_example_file(path: str, file_content: str):
    """
    Write file_content to file
    :param path: path to file
    :param file_content: content to write
    """
    with open(path, "w") as f:
        f.write(file_content)


def _check_and_create_dir(path: str):
    """
    Checks if such directory exists. If not, creates

    :param path: path to directory
    """
    if not os.path.exists(path):
        os.makedirs(path)


def _create_project_files(
    tree: Dict[str, ProjectFile], path: str, kwargs_container: dict
):
    """

    :param tree: project tree
    :param path: where to create files
    :param kwargs_container: kwargs for file content format
    """
    for key, value in tree.items():
        temp_path = os.path.join(path, key).format(**kwargs_container)
        if isinstance(value, ProjectFile):
            file_content = _read_file_template(value.path, kwargs_container)
            _write_example_file(temp_path, file_content)
        else:
            _check_and_create_dir(temp_path)
            _create_project_files(value, temp_path, kwargs_container)
