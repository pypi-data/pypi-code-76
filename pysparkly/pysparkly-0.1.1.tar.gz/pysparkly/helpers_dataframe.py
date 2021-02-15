"""
~ helpers_dataframe.py

Collection of functions to use over DataFrame.
"""
def parse_columns(df, included_pattern=None, excluded_pattern=None, columns=None, dtypes=None):
    """
    Get filtered set of columns from dataframe.

    :param DataFrame df:
    :param list(str) included_pattern: keep columns in this list.
    :param list(str) excluded_pattern: keep columns not int this list.
    :param list(str) columns: columns to parsed, by default use dataframe's columns.
    :param list(str) dtypes: types to keep, if 'None' keep all columns.
    """
    parsed_cols = columns if columns is not None else df.columns.copy()
    if dtypes is not None:
        parsed_cols = [col for col, coltype in df.dtypes if coltype in list(dtypes)]

    if excluded_pattern is not None and type(excluded_pattern) is list:
        parsed_cols = [col for col in parsed_cols if all(word not in col for word in excluded_pattern)]

    if included_pattern is not None and type(included_pattern) is list:
        parsed_cols = [col for col in parsed_cols if any(word in col for word in included_pattern)]

    parsed_cols = [col for col in parsed_cols if col in df.columns]
    return parsed_cols