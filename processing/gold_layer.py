from processing.spark_session import spark
from processing.quality_checks import validate_dataframe
from pyspark.sql.functions import year, avg, max, min, col, round as spark_round
from utils.logger import logger
import sys

try:
    # SELIC anual
    selic_df = (
        spark.read.format("delta").load("file:///app/data/silver/selic")
        .withColumn("ano", year("data"))
        .groupBy("ano")
        .agg(
            spark_round(avg("valor"), 2).alias("media_selic"),
            spark_round(max("valor"), 2).alias("max_selic"),
            spark_round(min("valor"), 2).alias("min_selic"),
        )
    )

    validate_dataframe(selic_df, "Gold SELIC")
    selic_df.coalesce(1).write.format("delta").mode("overwrite").option("overwriteSchema", "true").save("file:///app/data/gold/selic_anual")

    # IPCA anual
    ipca_df = (
        spark.read.format("delta").load("file:///app/data/silver/ipca")
        .withColumn("ano", year("data"))
        .groupBy("ano")
        .agg(
            spark_round(avg("valor"), 2).alias("media_ipca"),
        )
    )

    validate_dataframe(ipca_df, "Gold IPCA")
    ipca_df.coalesce(1).write.format("delta").mode("overwrite").option("overwriteSchema", "true").save("file:///app/data/gold/ipca_anual")

    # Cambio anual
    cambio_df = (
        spark.read.format("delta").load("file:///app/data/silver/cambio")
        .withColumn("ano", year("data"))
        .groupBy("ano")
        .agg(
            spark_round(avg("valor"), 4).alias("media_cambio"),
            spark_round(max("valor"), 4).alias("max_cambio"),
            spark_round(min("valor"), 4).alias("min_cambio"),
        )
    )

    validate_dataframe(cambio_df, "Gold Cambio")
    cambio_df.coalesce(1).write.format("delta").mode("overwrite").option("overwriteSchema", "true").save("file:///app/data/gold/cambio_anual")

    # CDI anual
    cdi_df = (
        spark.read.format("delta").load("file:///app/data/silver/cdi")
        .withColumn("ano", year("data"))
        .groupBy("ano")
        .agg(
            spark_round(avg("valor"), 2).alias("media_cdi"),
        )
    )

    validate_dataframe(cdi_df, "Gold CDI")
    cdi_df.coalesce(1).write.format("delta").mode("overwrite").option("overwriteSchema", "true").save("file:///app/data/gold/cdi_anual")

    # Taxa Real de Juros (SELIC - IPCA)
    taxa_real_df = (
        selic_df.join(ipca_df, "ano")
        .withColumn(
            "taxa_real",
            spark_round(col("media_selic") - col("media_ipca"), 2)
        )
        .select("ano", "media_selic", "media_ipca", "taxa_real")
    )

    validate_dataframe(taxa_real_df, "Gold Taxa Real")
    taxa_real_df.coalesce(1).write.format("delta").mode("overwrite").option("overwriteSchema", "true").save("file:///app/data/gold/taxa_real_anual")

    logger.info("Camada Gold completa")

except Exception as e:
    logger.error(f"Erro na Gold Layer: {e}")
    sys.exit(1)

finally:
    spark.stop()
