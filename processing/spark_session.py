from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

JARS = ",".join([
    "/app/jars/postgresql-42.7.3.jar",
    "/app/jars/spark-sql-kafka-0-10_2.12-3.5.0.jar",
    "/app/jars/kafka-clients-3.4.0.jar",
    "/app/jars/spark-token-provider-kafka-0-10_2.12-3.5.0.jar",
    "/app/jars/commons-pool2-2.11.1.jar",
])

builder = (
    SparkSession.builder
    .appName("BCB Data Lakehouse")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.driver.extraClassPath", JARS)
    .config("spark.executor.extraClassPath", JARS)
    .config("spark.jars", JARS)
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()

spark.sparkContext.setLogLevel("ERROR")