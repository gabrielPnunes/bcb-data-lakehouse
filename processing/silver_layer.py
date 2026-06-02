from processing.spark_session import spark
from processing.quality_checks import validate_dataframe

from pyspark.sql.functions import col, to_date
from pyspark.sql.types import DoubleType

from utils.logger import logger
import sys

try:
    df = spark.read.parquet("file:///app/data/bronze/selic")

    silver_df = (
        df
        .withColumn("data", to_date(col("data"), "dd/MM/yyyy"))
        .withColumn("valor", col("valor").cast(DoubleType()))
    )

    validate_dataframe(silver_df, "Silver Layer")

    silver_df.coalesce(1).write \
        .format("delta") \
        .mode("overwrite") \
        .save("file:///app/data/silver/selic")

    logger.info("Camada/medalion Silver Criada")

except Exception as e:
    logger.error(f"Erro na Silver Layer: {e}")
    sys.exit(1)

finally:
    spark.stop()