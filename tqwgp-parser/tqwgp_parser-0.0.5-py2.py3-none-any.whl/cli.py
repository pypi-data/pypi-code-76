# -*- coding: utf-8 -*-
"""
    tqwgp-parser.cli
    ~~~~~~~~~~~~~~~~~~~~~
    CLI for the TQWGP parser, allowing to parse JSON, Yaml and Toml.

    This is a Work-in-Progress.

    :copyright: (c) 2021 Yoan Tournade.
"""
import os

# TODO Implement TQWGP text-base document parsing CLI.
# Allowing to take various input format:
# - Python;
# - JSON;
# - Yaml;
# - Toml.


def load_project(project, file, project_path=None):
    # TODO Allows to load project by path. By require
    # to extract the project name from the path.
    if os.path.isdir(project):
        pathProject = project
        project = project.split("/")[-2 if project[-1] == "/" else -1]
    elif project_path:
        pathProject = project_path + "/" + project
    pathProject += "/"
    if not os.path.isdir(pathProject):
        raise ValueError("Project not found")
    if not os.path.exists(pathProject + file):
        raise ValueError("File not found")
    return pathProject, project
