from pydeco import add_method
from pyspark.sql.dataframe import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pysparkly import parse_columns
from typing import Callable, List


@add_method(DataFrame)
def with_columns(self: DataFrame, input_cols: List[str], func: Callable, output_cols: List[str] = None, udf_args: List[str] = None):
    """
    Apply an udf function to multiple columns

    :param self:
    :param input_cols: columns on which will be apply the function.
    :param output_cols: returned columns.
    :param func: function that will be apply on columns.
    :param udf_args: udf's arguments.
    """
    df = self
    output_cols = input_cols if output_cols is None else output_cols

    if udf_args is None:
        for input_col, output_col in zip(input_cols, output_cols):
            df = df.withColumn(output_col, func(input_col))
    else:
        for input_col, output_col, args in zip(input_cols, output_cols, udf_args):
            df = df.withColumn(output_col, func(input_col, args))
    return df


@add_method(DataFrame)
def order_columns(self: DataFrame, order: str = "asc", by_dtypes: bool = False):
    """
    Rearrange the columns in alphabetical order. 
    An option of rearrangement by dtypes is possible.

    :param self:
    :param by_dtypes: boolean to rearrange by dtypes first
    """
    if order not in ['asc', 'desc']:
        raise Exception("'{}' is not an acceptable ordering value, you can only use {'asc','desc'}".format(order))
    if by_dtypes:
        dtypes_dict = dict()
        for col, dtype in self.dtypes:
            dtypes_dict.setdefault(dtype, list())
            dtypes_dict[dtype].append(col)
        dtypes_dict = dict(sorted(dtypes_dict.items()))
        columns = [col for values in dtypes_dict.values()
                   for col in sorted(values)]
        return self.select(columns)

    else:
        return self.select(sorted(self.columns, reverse=False if order == "asc" else True))


@add_method(DataFrame)
def copy(
    self: DataFrame,
    input_cols: List[str],
    output_cols: List[str]
):
    """
    Copy columns in input_cols into output_cols.

    :param self:
    :param input_cols: copied columns
    :param output_cols: returned columns
    """
    columns = list(zip(input_cols, output_cols))
    for in_col, out_col in columns:
        self = self.withColumn(out_col, F.col(in_col))
    return self


@add_method(DataFrame)
def select_columns(
    self: DataFrame,
    included_pattern: List[str] = None,
    excluded_pattern: List[str] = None,
    columns: List[str] = None,
    dtypes: List[str] = None
):
    """
    Select specific columns from dataframe.

    :param DataFrame self:
    :param included_pattern: keep columns in this list.
    :param excluded_pattern: keep columns not int this list.
    :param columns: columns to parsed, by default use dataframe's columns.
    :param dtypes: types to keep, if 'None' keep all columns.
    """
    columns_to_keep = parse_columns(
        self, included_pattern, excluded_pattern, columns, dtypes)
    return self.select(*list(columns_to_keep))
