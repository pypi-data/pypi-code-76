# !/usr/bin/env python
# -*- coding:utf-8 -*-

import glob
import logging as log
import os
import pathlib as pt
from fnmatch import fnmatch
from typing import Any, IO

import yaml

from fameio.source.tools import log_and_raise

DISABLING_YAML_FILE_PREFIX = "IGNORE_"


class Loader(yaml.SafeLoader):
    """ Custom YAML Loader for `!include` constructor """
    def __init__(self, stream: IO) -> None:
        log.debug("Initialize custom Loader")
        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir
        super().__init__(stream)


class Args:
    def __init__(self, file_string, node_string):
        self.file_string = file_string
        self.node_string = node_string


def read_args(loader, args):
    """Returns two Strings to be interpreted as files to be read and a subnode_address from the given `args` """
    node_string = ""
    if isinstance(args, yaml.nodes.ScalarNode):
        file_string = loader.construct_scalar(args)
        log.debug("Found instance `ScalarNode` in {}".format(file_string))
    elif isinstance(args, yaml.nodes.SequenceNode):
        argument_list = loader.construct_sequence(args)
        if len(argument_list) not in [1, 2]:
            log_and_raise("!include supports but one or two arguments in list")
        elif len(argument_list) == 2:
            node_string = argument_list[1]
        file_string = argument_list[0]
        log.debug("Found instance `SequenceNode` in {}".format(file_string))
    elif isinstance(args, yaml.nodes.MappingNode):
        argument_map = loader.construct_mapping(args)
        for key, value in argument_map.items():
            if key.lower() == "file":
                file_string = value
            elif key.lower() == "node":
                node_string = value
            else:
                log_and_raise("!include supports only keys 'file' and 'node'")
        if not file_string:
            log_and_raise("!include: file must be specified.")
    else:
        log_and_raise("YAML node type not implemented: {}".format(args))
    return Args(file_string, node_string)


def split_nodes(node_string):
    """Returns a list of nodes created from the given `node_string`"""
    log.debug("Splitting given node_string `{}`".format(node_string))
    return node_string.split(":")


def get_files_from_string(root_path, file_string):
    """
    Returns a list of file paths matching the given `file_string` based on the given `root` directory.
    Ignores files starting with `DISABLING_YAML_FILE_PREFIX`
    """
    absolute_path = os.path.abspath(os.path.join(root_path, file_string))
    file_list = glob.glob(absolute_path)
    ignore_filter = "*" + DISABLING_YAML_FILE_PREFIX + "*"
    cleaned_file_list = []
    for file in file_list:
        if fnmatch(file, ignore_filter):
            log.debug("Ignoring file {} due to prefix {}".format(file, DISABLING_YAML_FILE_PREFIX))
        else:
            cleaned_file_list.append(file)
    if not cleaned_file_list:
        log.error("No valid files found for path {}".format(absolute_path))
    log.debug("Collected file(s) `{}` from given file_string `{}` in root path `{}`".format(cleaned_file_list, file_string, root_path))
    return cleaned_file_list


def read_data_from_file(file, node_address):
    """Returns data of the specified `node_address` from the specified `file`"""
    data = yaml.load(file, Loader)
    for node in node_address:
        if node:
            try:
                data = data[node]
            except KeyError:
                log_and_raise("'!include_node [{}, {}]': Cannot find '{}'.".format(file, node_address, node))
    log.debug("Searched file `{}` for node `{}`".format(file, node_address))
    return data


def join_data(new_data, previous_data):
    """Joins data from multiple files if both are in list format, otherwise returns """
    if not previous_data:
        return new_data
    if isinstance(new_data, list) and isinstance(previous_data, list):
        previous_data.extend(new_data)
        return previous_data
    else:
        log_and_raise("!include can only combine list-like elements from multiple files!")


def construct_include(loader: Loader, args: yaml.Node) -> Any:
    """
    Loads one or many YAML file(s) with specifications provided in `args` in different formats
    To load all content of a specified file, use:
        !include "path/to/file.yaml"
    To load only specific content (e.g. data of "Super:Sub:Node") from a given file, use:
        !include ["path/to/file.yml", "Super:Sub:Node"]
    For a slightly more verbose version of the above commands, use a dictionary argument:
        !include {"file":"path/to/file.yml", "node": "Super:Sub:Node"}

    Instead of "path/to/file.yaml" one can also use asterisks to select multiple files, e.g. "path/to/files/*.yaml"
    The given file path is either
      * relative to the path of the including YAML file, if it starts with a character other than "/"
      * an absolute path if its starts with "/"
    """
    args = read_args(loader, args)
    nodes = split_nodes(args.node_string)
    files = get_files_from_string(loader._root, args.file_string)

    joined_data = None
    for file_name in files:
        with open(file_name, 'r') as open_file:
            data = read_data_from_file(open_file, nodes)
            joined_data = join_data(data, joined_data)
    log.debug("Joined all files `{}` to joined data `{}`".format(files, joined_data))
    return joined_data


yaml.add_constructor('!include', construct_include, Loader)


def load_yaml(yaml_file_path):
    """Loads the yaml file from given `yaml_file_path` and returns its content"""
    log.info("Loading yaml from {}".format(yaml_file_path))
    with open(pt.Path(yaml_file_path), "r") as configfile:
        data = yaml.load(configfile, Loader=Loader)
    return data
