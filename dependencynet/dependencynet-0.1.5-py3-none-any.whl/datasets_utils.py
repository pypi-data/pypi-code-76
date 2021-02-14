"""
This module provides helpers to build the source datasets of the graph
"""
import os
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def extract_items_root(df, keys, id_pattern):
    logger.debug('extract_items_root keys=%s id_pattern=%s', keys, id_pattern)

    id_key = keys[-1]
    pos_key = 'pos'
    logger.debug('extract_items_root id_key=%s', id_key)

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

    logger.info('extract_items_root keys=%s id_pattern=%s => shape=%s', keys, id_pattern, items_df.shape)

    return items_df


def extract_items_non_root(df, keys, id_pattern, parent_df):
    logger.debug('extract_items_non_root keys=%s id_pattern=%s', keys, id_pattern)

    id_key = keys[-1]
    parent_keys = keys[0:-1]
    logger.debug('extract_items_non_root id_key=%s', id_key)

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

    items_df['id'] = items_df.apply(lambda row: id_pattern.format(id=row[pos_key], id_parent=row['id_parent']), axis=1)
    items_df['label'] = items_df.apply(lambda row: "%s %s" % (row['id'], row[id_key]), axis=1)

    logger.info('extract_items_root keys=%s id_pattern=%s => shape=%s', keys, id_pattern, items_df.shape)

    return items_df


def extract_hierarchy(df, schema):
    dfs = []
    logger.debug('extract_hierarchy schema=%s', schema)

    keys = schema.levels_keys()
    marks = schema.levels_marks()

    pattern = '%s{id:02d}' % marks[0]

    df_parent = extract_items_root(df, [keys[0]], pattern)
    dfs.append(df_parent)
    for i in range(1, len(keys)):
        df_i = extract_items_non_root(df, keys[0:i+1], '{id_parent}%s{id:02d}' % marks[i], df_parent)
        dfs.append(df_i)
        df_parent = df_i
    return dfs


def write_dataset(df, folder_name, dataset_name, sep=","):
    os.makedirs(folder_name, exist_ok=True)
    filename = os.path.join(folder_name, '%s.csv' % dataset_name)
    df.to_csv(filename, sep=sep, index=False)
    logger.info("dateset saved under name %s", filename)
