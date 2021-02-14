"""
This module provides helpers to manage the data schema
"""
import logging


class Schema:

    @classmethod
    def __init__(self, levels, resources, connections=None):
        self.levels = levels
        self.resources = resources
        self.connections = connections

    @classmethod
    def __repr__(self):
        return f"<Schema levels {self.levels} - resources {self.resources}>"

    @classmethod
    def levels_keys(self):
        return self.levels['keys']

    @classmethod
    def levels_marks(self):
        return self.levels['marks']

    @classmethod
    def resources_keys(self):
        return list(self.resources.keys())

    @classmethod
    def resource_mark(self, key):
        return self.resources[key]['mark']

    @classmethod
    def resource_definition(self, key):
        return self.resources[key]

    @classmethod
    def connections_pairs(self):
        return self.connections


class SchemaBuilder:
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self):
        self.levels = {'keys': [], 'marks': []}  # must keep order
        self.resources = {}
        self.connections = []

    @classmethod
    def level(self, label, mark):
        # TODI check whether mark is unique
        self.levels['keys'].append(label)
        self.levels['marks'].append(mark)
        return self

    @classmethod
    def resource(self, label, mark, role=None, connect_id_name=None, explode=False, delimiter='|'):
        # TODI check whether mark is unique
        # TODO which is key
        self.resources[label] = {'mark': mark,
                                 'role': role, 'connect_id_name': connect_id_name,
                                 'explode': explode, 'delimiter': delimiter}
        return self

    @classmethod
    def connect(self, left_key, right_key):
        # TODO unit test
        # TODO:  consistent wording for column labels and ids
        # TODO check whether columns exists and are inpout output
        # TODO structure for name, left, right
        self.connections.append((left_key, right_key))
        return self

    @classmethod
    def render(self):
        self.logger.info("rendering schema")
        return Schema(self.levels, self.resources, self.connections)
