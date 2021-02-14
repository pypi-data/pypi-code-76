"""
This module provides helpers to extract resources from source data
"""
import logging

import pandas as pd


class ResourcesLoader:
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self, schema, source_df, parent_df):
        self.schema = schema
        self.source_df = source_df
        self.parent_df = parent_df

    @classmethod
    def extract_all(self):
        dfs = {}
        self.logger.debug('extract_resource schema=%s', self.schema)

        keys = self.schema.resources_keys()
        for key in keys:
            mark = self.schema.resource_mark(key)
            loader = ResourcesLoader(self.schema, self.source_df, self.parent_df)
            df = loader.extract(key, '{id_parent}%s{id:02d}' % mark)
            dfs[key] = df
        return dfs

    @classmethod
    def extract(self, id_key, id_pattern):
        self.logger.debug(f'extract {id_key}')

        parent_keys = self.schema.levels_keys()
        # FIXME explode in schema ?

        source_columns = self.source_df.columns
        self.logger.debug(f'__extract_resource columns={source_columns}')

        if id_key not in source_columns:
            raise RuntimeError(f'{id_key} not found in datasource - columns:{source_columns}')

        self.logger.debug('__extract_resource key=%s id_pattern=%s', id_key, id_pattern)

        self.logger.debug('__extract_resource id_key=%s', id_key)

        pos_key = 'pos'

        # the key to this item : parent_keys + id_key
        reference_keys = parent_keys.copy()
        reference_keys.append(id_key)
        self.logger.debug('__extract_resource reference_keys=%s', reference_keys)
        items_df = self.source_df.drop_duplicates(subset=reference_keys)[reference_keys]

        # ignore item when no value is provided
        items_df.dropna(subset=[id_key], inplace=True)

        # unpack column consisting ina list of items into multiple lines
        explode = self.schema.resource_definition(id_key)['explode']
        if explode:  # TODO unpack
            delimiter = self.schema.resource_definition(id_key)['delimiter']
            items_df[id_key] = items_df[id_key].str.strip().str.split(delimiter)
            items_df = items_df.explode(id_key)

        items_df[pos_key] = items_df.groupby(parent_keys).cumcount()
        items_df[pos_key] = items_df[pos_key] + 1

        # enrich with parent id
        items_df = pd.merge(items_df, self.parent_df[parent_keys + ['id']], on=parent_keys)
        columns_mapping = {
            'id': 'id_parent'
        }
        items_df = items_df.rename(columns=columns_mapping)

        items_df['id'] = items_df.apply(
                    lambda row: id_pattern.format(id=row[pos_key], id_parent=row['id_parent']),
                    axis=1)
        items_df['label'] = items_df.apply(lambda row: "%s %s" % (row['id'], row[id_key]), axis=1)

        # if this attribute is in a connection, feed the id used as a connection id
        connect_id_name = self.schema.resource_definition(id_key)['connect_id_name']
        if connect_id_name is not None:
            items_df[connect_id_name] = items_df[id_key]

        self.logger.info('__extract_resource keys=%s id_pattern=%s => shape=%s',
                         reference_keys, id_pattern, items_df.shape)

        return items_df
