from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import expr

def postcode_to_inward_outward(df: DataFrame, pc_field: str, drop_orig:bool = True):
    """Given a field containing a postcode, creates new columns in the dataframe
    called outward_postcode_std and inward_postcode_std

    Original postcode can have spaces or not and be in any case

    Args:
        df (DataFrame): Spark Dataframe
        pc_field (str): Name of field containing postcode
    """    

    sql = f"upper(replace({pc_field}, ' ', ''))"
    df = df.withColumn("pc_nospace_temp__", expr(sql))

    # If the postcode is long enough, parse out inner outer
    # If it's too short, assume we only have the outer part
  
    sql = """
    case 
    when length(pc_nospace_temp__) >= 5 then left(pc_nospace_temp__, length(pc_nospace_temp__) - 3)
    else left(pc_nospace_temp__, 4)
    end
    """
    
    # sql = f"""left(pc_nospace_temp__, length(pc_nospace_temp__) - 3)"""
    df = df.withColumn("outward_postcode_std", expr(sql))

    sql = f"""right(pc_nospace_temp__, 3)"""

    sql = """
    case 
    when length(pc_nospace_temp__) >= 5 then right(pc_nospace_temp__, 3)
    else null 
    end
    """

    df = df.withColumn("inward_postcode_std", expr(sql))

    df = df.drop("pc_nospace_temp__")

    if drop_orig:
        df = df.drop(pc_field)

    return df