"""
This module provides helpers to extract levels from source data
"""
import logging

import pandas as pd


class LevelsLoader:
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self, schema, source_df):
        self.schema = schema
        self.source_df = source_df

    @classmethod
    def extract_all(self):
        dfs = []
        self.logger.debug('extract_hierarchy schema=%s', self.schema)

        keys = self.schema.levels_keys()
        marks = self.schema.levels_marks()

        pattern = '%s{id:02d}' % marks[0]

        df_parent = self.__extract_items_root(self.source_df, [keys[0]], pattern)
        dfs.append(df_parent)
        for i in range(1, len(keys)):
            df_i = self.__extract_items_non_root(self.source_df,
                                                 keys[0:i+1],
                                                 '{id_parent}%s{id:02d}' % marks[i],
                                                 df_parent)
            dfs.append(df_i)
            df_parent = df_i
        return dfs

    @classmethod
    def __extract_items_root(self, df, keys, id_pattern):
        self.logger.debug('extract_items_root keys=%s id_pattern=%s', keys, id_pattern)

        id_key = keys[-1]
        pos_key = 'pos'
        self.logger.debug('extract_items_root id_key=%s', id_key)

        items_df = df.drop_duplicates(subset=keys)[keys]

        def get_pos():
            i = 0
            while i < len(items_df.index):
                yield i
                i += 1

        items_df[pos_key] = pd.DataFrame(list(get_pos()), index=items_df.index)
        items_df[pos_key] = items_df[pos_key] + 1

        def format_id(p):
            id = id_pattern.format(id=p)
            return id

        items_df['id'] = items_df[pos_key].apply(lambda x: format_id(x))
        items_df['label'] = items_df.apply(lambda row: "%s %s" % (row['id'], row[id_key]), axis=1)

        self.logger.info('extract_items_root keys=%s id_pattern=%s => shape=%s', keys, id_pattern, items_df.shape)

        return items_df

    @classmethod
    def __extract_items_non_root(self, df, keys, id_pattern, parent_df):
        self.logger.debug('extract_items_non_root keys=%s id_pattern=%s', keys, id_pattern)

        id_key = keys[-1]
        parent_keys = keys[0:-1]
        self.logger.debug('extract_items_non_root id_key=%s', id_key)

        pos_key = 'pos'

        items_df = df.drop_duplicates(subset=keys)[keys]

        items_df[pos_key] = items_df.groupby(parent_keys).cumcount()
        items_df[pos_key] = items_df[pos_key] + 1

        # enrich with parent id
        items_df = pd.merge(items_df, parent_df[parent_keys + ['id']], on=parent_keys)
        columns_mapping = {
            'id': 'id_parent'
        }
        items_df = items_df.rename(columns=columns_mapping)

        items_df['id'] = items_df.apply(
                    lambda row: id_pattern.format(id=row[pos_key], id_parent=row['id_parent']),
                    axis=1)
        items_df['label'] = items_df.apply(lambda row: "%s %s" % (row['id'], row[id_key]), axis=1)

        self.logger.info('extract_items_root keys=%s id_pattern=%s => shape=%s', keys, id_pattern, items_df.shape)

        return items_df
