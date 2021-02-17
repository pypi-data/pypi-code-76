from pyspark.sql.functions import expr
from pyspark.sql.dataframe import DataFrame

def standardise_names(df:DataFrame, name_cols: list, drop_orig:bool=True):
    """Take a one or more name columns in a list and standardise the names
    so one name appears in each column consistently

    Args:
        df (DataFrame): Spark DataFrame
        name_cols (list): A list of columns that contain names, in order from first name to last name
        drop_orig (bool, optional): Drop the original columns after standardisation. Defaults to True.

    Returns:
        DataFrame: A Spark DataFrame with standardised name columns
    """


    name_col_joined = ", ".join(name_cols)
    surname_col_name = name_cols[-1]
    df = df.withColumn('name_concat', expr(f"concat_ws(' ', {name_col_joined})"))
    df = df.withColumn('name_concat', expr('lower(name_concat)'))
    df = df.withColumn('name_concat', expr("regexp_replace(name_concat, '[\\-\\.]', ' ')"))
    df = df.withColumn('name_arr', expr("split(name_concat, ' ')"))
    df = df.withColumn('surname_std', expr(f"case when {surname_col_name} is not null then element_at(name_arr,-1) else null end"))
    df = df.withColumn('forename1_std', expr("case when size(name_arr) > 1 then element_at(name_arr,1) else null end"))
    df = df.withColumn('forename2_std', expr("case when size(name_arr) > 2 then element_at(name_arr,2) else null end"))
    df = df.withColumn('forename3_std', expr("case when size(name_arr) > 3 then element_at(name_arr,3) else null end"))
    df = df.withColumn('forename4_std', expr("case when size(name_arr) > 4 then element_at(name_arr,4) else null end"))
    df = df.withColumn('forename5_std', expr("case when size(name_arr) > 5 then element_at(name_arr,5) else null end"))
    df = df.drop("name_arr", "name_concat")
    if drop_orig:
        for n in name_cols:
            df = df.drop(n)
    return df