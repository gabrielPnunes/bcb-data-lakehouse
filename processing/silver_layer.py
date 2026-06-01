from processing.spark_session import spark
from processing.quality_checks import validate_dataframe

from pyspark.sql.functions import year, avg

from utils.logger import logger
import sys

try:
    silver_df = (
        spark.read
        .format("delta")
        .load("file:///app/data/silver/selic")
    )

    gold_df = (
        silver_df
        .withColumn("ano", year("data"))
        .groupBy("ano")
        .agg(avg("valor").alias("media_selic"))
    )

    validate_dataframe(gold_df, "Gold Layer")

    gold_df.coalesce(1).write \
        .format("delta") \
        .mode("overwrite") \
        .save("file:///app/data/gold/selic_anual")

    logger.info("Camada/medalion Gold Criada")

except Exception as e:
    logger.error(f"Erro na Gold Layer: {e}")
    sys.exit(1)

finally:
    spark.stop()