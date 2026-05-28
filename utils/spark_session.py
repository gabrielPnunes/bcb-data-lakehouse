from pyspark.sql import SparkSession
import logging


def create_spark_session(app_name="BCB Lakehouse"):

    logging.getLogger("py4j").setLevel(logging.ERROR)

    spark = (
        SparkSession.builder
        .appName(app_name)
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark