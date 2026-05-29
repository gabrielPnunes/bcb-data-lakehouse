from processing.spark_session import spark

from pyspark.sql.functions import col, to_date
from pyspark.sql.types import DoubleType

from utils.logger import logger

df = spark.read.parquet("data/bronze/selic")

silver_df = (
    df
    .withColumn(
        "data",
        to_date(col("data"), "dd/MM/yyyy")
    )
    .withColumn(
        "valor",
        col("valor").cast(DoubleType())
    )
)

silver_df = silver_df.coalesce(1)

silver_df.write \
    .format("delta") \
    .mode("overwrite") \
    .save("data/silver/selic")

logger.info("Camada/medalion Silver Criada")