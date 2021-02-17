from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql import functions as f
import warnings


def null_out_values(df: DataFrame, colname: str, values_to_null):
    """Null out a list of undesirable values in a column
    Useful for columns that mostly contain valid data but occasionally
    contain other values such as 'unknown'
    Args:
        df (DataFrame): The dataframe to clean
        colname (string): The name of the column to clean
        values_to_null: A list of values to be nulled.

    Returns:
        DataFrame: The cleaned dataframe with incoming column overwritten
    """

    if len(values_to_null) == 0:
        return df

    values_to_null_string = [f'"{v}"' for v in values_to_null]
    values_to_null_joined = ", ".join(values_to_null_string)

    case_statement = f"""
    CASE
    WHEN {colname} in ({values_to_null_joined}) THEN NULL
    ELSE {colname}
    END
    """

    df = df.withColumn(colname, f.expr(case_statement))

    return df


def null_out_values_array(df: DataFrame, array_colname: str, values_to_null: list):
    """Null out a user defined list of undesirable values in a column that contains an array of values
    Useful for columns that mostly contain valid data but occasionally
    contain other values such as 'unknown'
   
    Args:
        df (DataFrame): The dataframe to clean
        colname (string): The name of the column to clean
        values_to_null (list): A list of values to be nulled.
    Returns:
        DataFrame: The cleaned dataframe with column containing array that has values in values_to_null nulled
    """
    if len(values_to_null) > 0:

        if str((dict(df.dtypes)[array_colname])).startswith("array"):

            array_args = [f.lit(v) for v in values_to_null]
            df = df.withColumn("vals_to_remove", f.array(*array_args))
            df = df.withColumn(
                array_colname, f.expr(f"array_except({array_colname}, vals_to_remove)")
            )
            df = df.drop("vals_to_remove")

        else:
            # if column is not an array fire up a warning
            warnings.warn(
                f""" column {array_colname} is not an array. Please use function null_out_values instead  """
            )

    return df


def remove_special_character_values_within_array(df: DataFrame, array_colname: str):
    """Null out a preset list of undesirable values in a column that contains an array of values
    Useful for columns that mostly contain valid data but occasionally
    contain other values such as newlines etc
    
    Args:
        df (DataFrame): The dataframe to clean
        colname (string): The name of the column to clean
        
    Returns:
        DataFrame: The cleaned dataframe with column containing array that has special character values nulled
    """

    special_character_values = [
        "'",
        '""',
        "\\n",
        "\\",
        '"',
        '""',
        "\\t",
        "\\n",
        "\\r",
        "\\b",
        "\/",
        "\n",
        "\r",
        "\b"
    ]

    return null_out_values_array(df, array_colname, special_character_values)
