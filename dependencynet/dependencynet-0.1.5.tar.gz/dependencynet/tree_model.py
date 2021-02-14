"""
This module provides helpers to setup the data model tree
"""
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class TreeModel:
    tree = None

    @classmethod
    def __init__(self, tree):
        self.tree = tree
        pass

    @classmethod
    def __repr__(self):
        return self.tree.__repr__()


class TreeModelBuilder():
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self):
        pass

    @classmethod
    def from_canonical(self, levels_datasets, resources_datasets):
        self.levels_datasets = levels_datasets
        self.resources_datasets = resources_datasets
        return self

    @classmethod
    def with_schema(self, schema):
        logger.debug(f'with_schema {schema}')
        self.schema = schema
        return self

    @classmethod
    def render(self):
        levels_dfs = self.levels_datasets
        resources_dfs = self.resources_datasets
        keys = self.schema.levels_keys()
        tree = self.__build_tree(levels_dfs, keys, resources_dfs)
        return TreeModel(tree)

    # ---- private

    @classmethod
    def __build_tree(self, levels_dfs, keys, resources_dfs):
        tree = defaultdict(dict)
        elt0_name = "%s_dict" % keys[0]
        tree[elt0_name]

        l0 = levels_dfs[0].groupby('id')
        for k0, v0 in l0:
            records = v0.to_dict('records')
            tree[elt0_name][k0] = records[0]
            elt1_name = "%s_dict" % keys[1]
            tree[elt0_name][k0][elt1_name] = {}

            df1 = levels_dfs[1]
            l1 = df1[df1['id_parent'] == k0].groupby('id')
            for k1, v1 in l1:
                records = v1.to_dict('records')
                tree[elt0_name][k0][elt1_name][k1] = records[0]
                elt2_name = "%s_dict" % keys[2]
                tree[elt0_name][k0][elt1_name][k1][elt2_name] = {}

                df2 = levels_dfs[2]
                l2 = df2[df2['id_parent'] == k1].groupby('id')
                for k2, v2 in l2:
                    records = v2.to_dict('records')
                    tree[elt0_name][k0][elt1_name][k1][elt2_name][k2] = records[0]

                    if resources_dfs is not None:
                        parent_tree = tree[elt0_name][k0][elt1_name][k1][elt2_name][k2]
                        logger.debug(f'{len(resources_dfs)}')
                        for name, dfr in resources_dfs.items():
                            r = dfr[dfr['id_parent'] == k2].groupby('id')
                            eltr_name = "%s_dict" % name
                            parent_tree[eltr_name] = {}
                            for kr, vr in r:
                                records = vr.to_dict('records')
                                parent_tree[eltr_name][kr] = records[0]

        return tree
