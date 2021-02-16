import json
import pyspark
import IPython


def get_dbutils(spark):
    dbutils = None
    if spark.conf.get("spark.databricks.service.client.enabled") == "true":
        from pyspark.dbutils import DBUtils

        dbutils = DBUtils(spark)
    else:
        import IPython

        dbutils = IPython.get_ipython().user_ns["dbutils"]
    return dbutils


def get_context():
    from pyspark.sql.session import SparkSession

    spark = SparkSession.builder.getOrCreate()
    dbutils = get_dbutils(spark)
    context = json.loads(
        dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    )
    return context
