from pyspark.sql import SparkSession
from utils.logger import logger

spark = (
    SparkSession.builder
    .appName("BCB Bronze Layer")
    .getOrCreate()
)

df = spark.read.csv(
    "data/raw/selic/selic.csv",
    header=True,
    inferSchema=True
)

df.write.mode("overwrite").parquet(
    "data/bronze/selic"
)

logger.info("Camada/medalion Bronze Criada")