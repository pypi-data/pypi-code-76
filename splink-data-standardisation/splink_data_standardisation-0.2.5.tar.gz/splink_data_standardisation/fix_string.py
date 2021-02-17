from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import expr, regexp_replace, col

def fix_zero_length_strings(df:DataFrame):
    """Convert any zero length strings or strings that contain only whitespace to a true null

    Args:
        df (DataFrame): Input Spark dataframe

    Returns:
        DataFrame: Spark Dataframe with clean strings
    """    

    string_cols = [item[0] for item in df.dtypes if item[1].startswith('string')]

    stmt = """
    case 
    when trim({c}) = '' then null
    else trim({c})
    end
    """

    for c in string_cols:
        df = df.withColumn(c, expr(stmt.format(c=c)))

    return df

def remove_leading_zeros(df:DataFrame, colname:str, newname:str, drop_orig:bool=True):
    """Remove leading zeros from a column

    Args:
        df (DataFrame): Input Spark dataframe
        colname (str): Column name of column to remove leading zeros
        newname (str): Column name of output column
        drop_orig (bool, optional): Drop original column. Defaults to True.
    """    

    df = df .withColumn(newname, regexp_replace(col(colname), "^0+", ""))

    if drop_orig:
        if colname != newname:
            df = df.drop(colname)

    return df

