from __future__ import print_function
import os
import logging
import time
from collections import defaultdict
from xml.etree import cElementTree as ET

import click
from globster import Globster

from mcutk.apps.projectbase import ProjectBase
from mcutk.apps import appfactory
from mcutk.sdk_manifest import SDKManifest
from mcutk.exceptions import ProjectNotFound, ProjectParserError

LOGGER = logging.getLogger(__name__)

TOOLCHAINS = [
    'iar',
    'mdk',
    'mcux',
    'armgcc',
    'xcc',
    'codewarrior',
    'lpcx',
]


EXCLUDE_DIR_NAME = [
    'log/',
    'debug/',
    'obj/',
    'release/',
    '.debug/',
    '.release/',
    'RTE/',
    'settings/'
    '.git/',
    '__pycache__/',
    'flexspi_nor_debug/',
    'flexspi_nor_release/'
]

IDE_INS = [appfactory(toolname) for toolname in TOOLCHAINS]
Exclude_Matcher = Globster(EXCLUDE_DIR_NAME)

def identify_project(path, toolname=None, manifest_check=True):
    """ Identify and return initiliazed project instance.

    Arguments:
        path {str} -- project path

    Keyword Arguments:
        toolname {str} -- if toolname is given, it will try to load
            the project with the tool. (default: None)
        manifest_check (bool, optional): Check example is enabled in MCUXpressoIDE manifest. Default True.

    Returns:
        Project object
    """
    if toolname:
        cls = appfactory(toolname)
        return cls.Project.frompath(path)

    prj = None
    for cls in IDE_INS:
        try:
            prj = cls.Project.frompath(path)
            if prj and prj.idename == 'mcux' and manifest_check \
                and not prj.is_enabled:
                logging.debug("not enabled in manifest.")
                return None
            break
        except ProjectParserError as err:
            logging.warning(str(err))
        except ET.ParseError as err:
            logging.error("Bad project: %s, Reason: %s", path, err)
        except ProjectNotFound:
            pass

    return prj


def find_projects_from_dir(dirs, recursive=False, manifest_check=True):
    """Find projects from a list of directories.

    Args:
        dirs ([list]): list of directories to search
        recursive (bool, optional): Recursive to search. Defaults to False.
        manifest_check (bool, optional): Check example is enabled in manifest. Default False..

    Returns:
        [type]: [description]
    """
    projects = defaultdict(list)
    for dir in dirs:
        project = identify_project(dir, manifest_check=manifest_check)
        if project:
            projects[project.idename].append(project)

        if recursive:
            for root, folders, _ in os.walk(dir, topdown=True):
                for folder in folders:
                    if Exclude_Matcher.match(folder):
                        continue

                    path = os.path.join(root, folder)
                    project = identify_project(path, manifest_check=manifest_check)
                    if project:
                        projects[project.idename].append(project)
    return projects


def find_projects_from_manifests(sdk_dir, manifests=None):
    """Find projects by searching in SDK manifest."""
    if not manifests:
        if not sdk_dir:
            raise ValueError('invalid sdk_dir')
        manifests = SDKManifest.find(sdk_dir)

    if not manifests:
        return

    projects = defaultdict(list)
    for manifest in manifests:
        examples = manifest.dump_examples()
        search_folders = [sdk_dir + "/" + example['path'] for example in examples]
        ProjectBase.SDK_MANIFEST = manifest
        manifest_prjs = find_projects_from_dir(search_folders, recursive=True)
        if manifest_prjs:
            for key, value in manifest_prjs.items():
                projects[key].extend(value)
    return projects


def find_projects(root_dir, recursive=True, include_tools=None, exclude_tools=None, manifests_dir=None):
    """Find projects in specific directory.

    Arguments:
        root_dir {string} -- root directory
        recursive {bool} -- recursive mode
        include_tools {list} -- only include specifices tools
        exclude_tools {list} -- exlucde specifices tools
    Returns:
        {dict} -- key: toolchain name, value: a list of Project objects.

    Example:
        >> ps = find_projects("C:/code/mcu-sdk-2.0", True)
        >> ps
        {
            'iar': [<Project Object at 0x1123>, <Project Object at 0x1124>],
            'mdk': [<Project Object at 0x1123>, <Project Object at 0x1124>],
            ...
        }
    """
    print('Process scanning')
    sdk_manifest = None
    sdk_root = None
    manifest_list = None
    s_time = time.time()
    # To speed up the performance, use a workaround to find the manifest file.
    if os.path.basename(os.path.abspath(root_dir)) == 'boards':
        sdk_root = os.path.dirname(root_dir)
    else:
        sdk_root = root_dir

    # try to find manifest in sdk root
    sdk_manifest = SDKManifest.find_max_version(sdk_root)
    if sdk_manifest:
        LOGGER.debug("Found SDK Manifetst: %s", sdk_manifest)
        ProjectBase.SDK_MANIFEST = sdk_manifest
        ProjectBase.SDK_ROOT = sdk_root.replace('\\', '/') + "/"
    else:
        # assume manifest files is saved in ./manifests
        if not manifests_dir:
            manifests_dir = os.path.join(sdk_root, 'manifests')
        manifest_list = SDKManifest.find(manifests_dir)

    # multiple manifests, use manifest to search projects
    if manifest_list:
        print('Multiple manifest files were found in %s' % manifests_dir)
        projects = find_projects_from_manifests(sdk_root, manifests=manifest_list)
    else:
        projects = find_projects_from_dir([root_dir], recursive=recursive)

    if projects:
        if include_tools:
            projects = {k: v for k, v in projects.items() if k in include_tools}

        elif exclude_tools:
            for toolname in exclude_tools:
                if toolname in projects:
                    projects.pop(toolname)

    e_time = time.time()
    count = 0
    for toolname, prjs in projects.items():
        length = len(prjs)
        count += length

    click.echo("Found projects total {0}, cover {1} toolchains. Used {2:.2f}(s)".format(
        count, len(projects), e_time-s_time))

    for toolname, prjs in projects.items():
        length = len(prjs)
        click.echo(" + {0:<10}  {1}".format(toolname, length))

    return projects, count
