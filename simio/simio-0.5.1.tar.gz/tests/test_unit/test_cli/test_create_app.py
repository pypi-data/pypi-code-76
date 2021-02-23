import os
from unittest.mock import patch, Mock, call

import pytest

from simio.cli.create_app import create_project, _create_project_files, ProjectFile


class MockProjectFile(ProjectFile):
    def __init__(self, path):
        super().__init__(path)
        self.path = path


@pytest.mark.parametrize(
    "project_tree, kwargs_container, check_and_create_dir_calls, read_file_template_calls, write_example_file_calls",
    (
        # fmt: off
        (
            {
                "{project_name}": {
                    "__init__.py": MockProjectFile(path="files/module_init.sim"),
                }
            },
            {"project_name": "myproj"},
            [call('usr/folder/myproj')],
            [call('files/module_init.sim', {'project_name': 'myproj'})],
            [call('usr/folder/myproj/__init__.py', 'content-{project_name}')],
        ),
        (
            {
                "{project_name}": {
                    "__init__.py": MockProjectFile(path="files/module_init.sim"),
                    "handlers": {
                        "handler.py": MockProjectFile(path="files/handler")
                    }
                },
                "Makefile": MockProjectFile(path="files/make"),
                "run.sim.py": MockProjectFile(path="files/run.sim")
            },
            {"project_name": "mpr"},
            [call('usr/folder/mpr'), call('usr/folder/mpr/handlers')],
            [
                call('files/module_init.sim', {'project_name': 'mpr'}),
                call('files/handler', {'project_name': 'mpr'}),
                call('files/make', {'project_name': 'mpr'}),
                call('files/run.sim', {'project_name': 'mpr'})
            ],
            [
                call('usr/folder/mpr/__init__.py', 'content-{project_name}'),
                call('usr/folder/mpr/handlers/handler.py', 'content-{project_name}'),
                call('usr/folder/Makefile', 'content-{project_name}'),
                call('usr/folder/run.sim.py', 'content-{project_name}')
            ],
        ),
        # fmt: on
    ),
)
def test_create_project_files(
    project_tree,
    kwargs_container,
    check_and_create_dir_calls,
    read_file_template_calls,
    write_example_file_calls,
):
    check_and_create_dir_mock = Mock()
    read_file_template_mock = Mock(return_value="content-{project_name}")
    write_example_file_mock = Mock()
    with patch(
        "simio.cli.create_app._check_and_create_dir", check_and_create_dir_mock
    ), patch(
        "simio.cli.create_app._read_file_template", read_file_template_mock
    ), patch(
        "simio.cli.create_app._write_example_file", write_example_file_mock
    ):
        _create_project_files(project_tree, "usr/folder", kwargs_container)

        assert check_and_create_dir_mock.call_args_list == check_and_create_dir_calls
        assert read_file_template_mock.call_args_list == read_file_template_calls
        assert write_example_file_mock.call_args_list == write_example_file_calls
