from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import expr, regexp_replace, col
import pyspark.sql.functions as f

# This fixes a problem where athena can't handle a parquet file with a zero length array
# so [None] is fine, and so is None, but [] is not
# See here: https://forums.aws.amazon.com/thread.jspa?messageID=874178&tstart=0
# A reprex is here https://gist.github.com/RobinL/0692e2cd266483b3088646206aa8be62
def fix_zero_length_arrays(df: DataFrame):
    """For every field of type array, turn zero length arrays into true nulls

    Args:
        df (DataFrame): Input Spark dataframe

    Returns:
        DataFrame: Spark Dataframe with clean arrays
    """

    array_cols = [
        (item[0], not(item[1].startswith("array<array")))
        for item in df.dtypes
        if item[1].startswith("array")
    ]

    for c, trim in array_cols:
        df = fix_zero_length_array(c, df, trim)

    return df


def fix_zero_length_array(column_name: str, df: DataFrame, trim: bool = True):
    """Turn zero length arrays into true nulls for a single column

    Args:
        column_name (str): Col name
        df (DataFrame): Dataframe in which the column resides
        trim (bool): Flag to trim whitespace (defaults to True)
    """

    trim_expr = "and trim(x) != ''" if trim else ""

    stmt = f"""
    case
    when size(filter({column_name}, x -> x is not null {trim_expr})) > 0
    then filter({column_name}, x -> x is not null {trim_expr})
    else null
    end
    """

    df = df.withColumn(column_name, expr(stmt))
    return df


def remove_leading_zeros_array(df: DataFrame, array_colname: str):
    """Remove leading zeros from values of an array column
    Args:
        df (DataFrame): Input Spark dataframe
        array_colname (str): Column name of array column to remove leading zeros from values
   
    """

    stmt = f""" 
    
    TRANSFORM({array_colname}, x -> regexp_replace(x, "^0+", "")) 
    
    """

    df = df.withColumn(array_colname, f.expr(stmt))

    return df
