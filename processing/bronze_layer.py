from pyspark.sql import SparkSession
from utils.logger import logger
import sys

spark = (
    SparkSession.builder
    .appName("BCB Bronze Layer")
    .getOrCreate()
)

try:
    df = spark.read.csv(
        "file:///app/data/raw/selic/selic.csv",
        header=True,
        inferSchema=True
    )

    df.write.mode("overwrite").parquet(
        "file:///app/data/bronze/selic"
    )

    logger.info("Camada/medalion Bronze Criada")

except Exception as e:
    logger.error(f"Erro na Bronze Layer: {e}")
    sys.exit(1)

finally:
    spark.stop()