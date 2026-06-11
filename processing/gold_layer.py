from processing.spark_session import spark
from processing.quality_checks import validate_dataframe
from config.settings import SILVER, GOLD
from pyspark.sql.functions import year, avg, max, min, last, col, round as spark_round, sum as spark_sum, exp, log
from pyspark.sql.window import Window
from utils.logger import logger
import sys


def write_gold(df, name: str, path: str):
    validate_dataframe(df, f"Gold {name}")
    df.coalesce(1).write         .format("delta")         .mode("overwrite")         .option("overwriteSchema", "true")         .save(path)
    logger.info(f"Gold {name} criada com sucesso")


try:
    # SELIC — media anual + ultimo valor diario
    selic_silver = spark.read.format("delta").load(SILVER["selic"])
    selic_silver = selic_silver.withColumn("ano", year("data"))

    selic_window = Window.partitionBy("ano").orderBy("data")

    selic_df = (
        selic_silver
        .withColumn("ultimo_selic", last("valor").over(selic_window))
        .groupBy("ano")
        .agg(
            spark_round(avg("valor"), 2).alias("media_selic"),
            spark_round(max("valor"), 2).alias("max_selic"),
            spark_round(min("valor"), 2).alias("min_selic"),
            spark_round(last("ultimo_selic"), 2).alias("ultimo_selic"),
        )
    )
    write_gold(selic_df, "SELIC", GOLD["selic_anual"])

    # IPCA — media, acumulado por soma e acumulado por juros compostos
    ipca_silver = spark.read.format("delta").load(SILVER["ipca"])
    ipca_silver = ipca_silver.withColumn("ano", year("data"))

    ipca_df = (
        ipca_silver
        .withColumn("log_fator", log(1 + col("valor") / 100))
        .groupBy("ano")
        .agg(
            spark_round(avg("valor"), 2).alias("media_ipca"),
            spark_round(spark_sum("valor"), 2).alias("ipca_acumulado_simples"),
            spark_round((exp(spark_sum("log_fator")) - 1) * 100, 2).alias("ipca_acumulado"),
        )
    )
    write_gold(ipca_df, "IPCA", GOLD["ipca_anual"])

    # CAMBIO — media, max, min e ultimo valor do ano
    cambio_silver = spark.read.format("delta").load(SILVER["cambio"])
    cambio_silver = cambio_silver.withColumn("ano", year("data"))

    cambio_window = Window.partitionBy("ano").orderBy("data")

    cambio_df = (
        cambio_silver
        .withColumn("ultimo_cambio", last("valor").over(cambio_window))
        .groupBy("ano")
        .agg(
            spark_round(avg("valor"), 4).alias("media_cambio"),
            spark_round(max("valor"), 4).alias("max_cambio"),
            spark_round(min("valor"), 4).alias("min_cambio"),
            spark_round(last("ultimo_cambio"), 4).alias("ultimo_cambio"),
        )
    )
    write_gold(cambio_df, "Cambio", GOLD["cambio_anual"])

    # CDI — media anual + ultimo valor diario
    cdi_silver = spark.read.format("delta").load(SILVER["cdi"])
    cdi_silver = cdi_silver.withColumn("ano", year("data"))

    cdi_window = Window.partitionBy("ano").orderBy("data")

    cdi_df = (
        cdi_silver
        .withColumn("ultimo_cdi", last("valor").over(cdi_window))
        .groupBy("ano")
        .agg(
            spark_round(avg("valor"), 2).alias("media_cdi"),
            spark_round(last("ultimo_cdi"), 2).alias("ultimo_cdi"),
        )
    )
    write_gold(cdi_df, "CDI", GOLD["cdi_anual"])

    # Taxa Real — ultimo SELIC - IPCA acumulado por juros compostos
    taxa_real_df = (
        selic_df.join(ipca_df, "ano")
        .withColumn("taxa_real", spark_round(col("ultimo_selic") - col("ipca_acumulado"), 2))
        .select("ano", "ultimo_selic", "ipca_acumulado", "taxa_real")
    )
    write_gold(taxa_real_df, "Taxa Real", GOLD["taxa_real_anual"])

    # IPCA 12 meses — juros compostos dos ultimos 12 registros mensais
    from pyspark.sql.functions import desc, row_number
    from pyspark.sql.window import Window as W

    ipca_raw = spark.read.format("delta").load(SILVER["ipca"])

    window_row = W.orderBy(desc("data"))
    ipca_12m = (
        ipca_raw
        .withColumn("rn", row_number().over(window_row))
        .filter(col("rn") <= 12)
        .agg(
            spark_round((exp(spark_sum(log(1 + col("valor") / 100))) - 1) * 100, 2).alias("ipca_12m")
        )
    )

    from pyspark.sql.functions import lit
    ipca_12m = ipca_12m.withColumn("ano", lit(2026))
    write_gold(ipca_12m, "IPCA 12M", GOLD["ipca_12m"])

    logger.info("Camada Gold completa")

except Exception as e:
    logger.error(f"Erro na Gold Layer: {e}")
    sys.exit(1)

finally:
    spark.stop()
