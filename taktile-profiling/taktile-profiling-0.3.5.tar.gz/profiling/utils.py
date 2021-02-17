from typing import Any, Dict, List

import numpy as np
import pandas
from pandas.api.types import (
    is_bool_dtype,
    is_categorical_dtype,
    is_float_dtype,
    is_integer_dtype,
    is_object_dtype,
)


def df_to_json_table(df, *args, **kwargs):
    """Create a json table from a pandas dataframe

    Parameters
    ----------
    df : pd.Dataframe
        Input dataframe
    *args: passed on to df.to_dict
    **kwargs: passed on to df.to_dict

    Returns
    -------
    string
        json encoded and versioned table
    """

    version = "tktl v0.1"

    string = df.to_json(*args, orient="split", **kwargs, index=False)

    return string[:-1] + ',"version":"' + version + '"}'


def df_to_dict(df):
    """Create a dictionary from pandas dataframes
    Types are converted to native Python types using pandas' built-in
    mapping (see pd.DataFrame.to_dict()).
    Parameters
    ----------
    df : pd.Dataframe
        Input dataframe
    Returns
    -------
    dict
        Dictionary with variable names as keys and columns as lists.
    """
    dataset = {}
    df = df.replace({np.nan: None})
    for var, values in df.to_dict().items():
        dataset[var] = list(values.values())
    return dataset


def create_description(series, n_options=100) -> Dict:
    """Create an input description for a series for use in dropdowns

    Parameters
    ----------
    series : pd.Series
        Pandas Series to be described
    n_options : int, optional
        Number of options for dropdown menus, by default 100

    Returns
    -------
    dict
        Description of the series
    """
    col_type = series.dtype

    if is_categorical_dtype(col_type):
        options = list(series.cat.categories)[:n_options]
        field_type = "category"

    elif is_object_dtype(col_type):
        value_counts = series.value_counts(dropna=True)
        options = value_counts.keys().to_list()[:n_options]
        field_type = "category"

    elif is_bool_dtype(col_type):
        options = [True, False]
        field_type = "bool"

    elif is_integer_dtype(col_type):
        options = None
        field_type = "integer"

    elif is_float_dtype(col_type):
        options = None
        field_type = "float"

    else:
        options = None
        field_type = str(col_type)

    input_description = {
        "name": series.name,
        "field_type": field_type,
        "options": options,
    }

    return input_description


def vega_sanitize(var, datatype=None):
    """Sanitize string for use as variable name in Vega-Lite/Altair

    For background, see: https://github.com/altair-viz/altair/issues/284
    """
    var = var.replace(".", "\\.")
    var = var.replace("[", "\\[")
    var = var.replace("]", "\\]")
    if datatype:
        var = var + ":" + datatype
    return var


def input_schema_to_pandas(value: Any, names: List[str]) -> pandas.DataFrame:
    print(names, value)
    if isinstance(value, pandas.DataFrame):
        value.columns = names
        return value
    else:
        return pandas.DataFrame(value, columns=names)
