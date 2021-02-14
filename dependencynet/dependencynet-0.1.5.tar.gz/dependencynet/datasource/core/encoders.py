"""
This module provides helpers to encode base classes
"""
from json import JSONEncoder


class SchemaEncoder(JSONEncoder):
    def default(self, o):
        properties = {'levels': o.levels, 'resources': o.resources}
        return properties

    # def from_json(json_object):
    #    if 'fname' in json_object:
    #       return FileItem(json_object['fname'])
    # f = JSONDecoder(object_hook = from_json).decode('{"fname": "/foo/bar"}')


class TreeModelEncoder(JSONEncoder):
    def default(self, o):
        return o.tree

    # def from_json(json_object):
    #    if 'fname' in json_object:
    #       return FileItem(json_object['fname'])
    # f = JSONDecoder(object_hook = from_json).decode('{"fname": "/foo/bar"}')
