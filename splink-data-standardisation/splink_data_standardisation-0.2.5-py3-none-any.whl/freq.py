
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql import functions as f


def null_out_entries_with_freq_above_n(df: DataFrame, colname: str, n: int, spark:SparkSession):
    """Null out values above a certain frequency threshold

    Useful for columns that mostly contain valid data but occasionally
    contain other values such as 'unknown'

    Args:
        df (DataFrame): The dataframe to clean
        colname (string): The name of the column to clean
        n (int): The maximum frequency allowed.  Any values with a frequency higher than n will be nulled out
        spark (SparkSession): The spark session

    Returns:
        DataFrame: The cleaned dataframe with incoming column overwritten
    """    

    # Possible that a window function would be better than the following approach
    # But I think both require a shuffle so possibly doesn't make much difference

    df.createOrReplaceTempView("df")

    sql = f"""
    select {colname} as count
    from df
    group by {colname}
    having count(*) > {n}
    """

    df_groups = spark.sql(sql)

    collected = df_groups.collect()

    values_to_null = [row["count"] for row in collected]
    
    if len(values_to_null) == 0:
        return df
    
    values_to_null = [f'"{v}"' for v in values_to_null]
    values_to_null_joined = ", ".join(values_to_null)

    case_statement = f"""
    CASE
    WHEN {colname} in ({values_to_null_joined}) THEN NULL
    ELSE {colname}
    END
    """

    df = df.withColumn(colname, f.expr(case_statement))

    return df
