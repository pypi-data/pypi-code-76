"""
This module provides helpers to store the model
"""
import logging
from os import path, makedirs
import json

from dependencynet.datasource.core.encoders import SchemaEncoder, TreeModelEncoder


class ModelStorageService:
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self, root_location, sep=','):
        self.root_location = root_location
        self.sep = sep

    @classmethod
    def load(self, schema, filename, sep=','):
        # TODO
        pass

    @classmethod
    def save(self, model, model_name='current'):
        try:
            makedirs(self.root_location, exist_ok=True)
            model_folder = path.join(self.root_location, model_name)
            makedirs(model_folder, exist_ok=True)  # TODO clean before replace
            self.logger.info("model folder is %s", model_folder)
            self.__save_schema(model_folder, model)
            self.__save_levels(model_folder, model)
            self.__save_resources(model_folder, model)
            self.__save_tree(model_folder, model)
        except Exception as err:
            self.logger.error('Model not saved. Reason: %s', err)

    # ---- private

    @classmethod
    def __save_schema(self, model_folder, model):
        self.logger.debug("__save_schema")
        filename = path.join(model_folder, 'schema.json')
        with open(filename, "w") as fh:
            json.dump(model.schema, fh, cls=SchemaEncoder, indent=2)
            self.logger.info("schema saved under name %s", filename)

    @classmethod
    def __save_levels(self, model_folder, model):
        names = model.schema.levels_keys()
        self.logger.debug(f"__save_levels names={names}")

        def save_level(df, name):
            self.logger.debug(f"save_level {name}")
            filename = path.join(model_folder, f'{name}.csv')
            df.to_csv(filename, sep=self.sep, index=False)
            self.logger.info("dateset saved under name %s", filename)

        [save_level(model.levels_datasets[i], names[i]) for i in range(len(names))]

    @classmethod
    def __save_resources(self, model_folder, model):
        names = model.schema.resources_keys()
        self.logger.debug(f"__save_resources names={names}")

        def save_resource(df, name):
            self.logger.debug(f"save_resource {name}")
            filename = path.join(model_folder, f'{name}.csv')
            df.to_csv(filename, sep=self.sep, index=False)
            self.logger.info("dateset saved under name %s", filename)

        [save_resource(model.resource_dataset(name), name) for name in names]

    @classmethod
    def __save_tree(self, model_folder, model):
        filename = path.join(model_folder, 'tree.json')
        with open(filename, "w") as fh:
            json.dump(model.tree_model, fh, cls=TreeModelEncoder, indent=2)
            self.logger.info("tree saved under name %s", filename)


class SchemaStorage:
    logger = logging.getLogger(__name__)

    @staticmethod
    def load(self, schema, filename, sep=','):
        # TODO
        pass

    @staticmethod
    def save(self, schema, filename, sep=','):
        # TODO
        pass
