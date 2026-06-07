from processing.spark_session import spark
from processing.quality_checks import validate_dataframe
from pyspark.sql.functions import col, to_date, pow, round as spark_round
from pyspark.sql.types import DoubleType
from utils.logger import logger
import sys

SERIES = {
    "selic":  {"date_format": "dd/MM/yyyy", "annualize": True},
    "ipca":   {"date_format": "dd/MM/yyyy", "annualize": False},
    "cambio": {"date_format": "dd/MM/yyyy", "annualize": False},
    "cdi":    {"date_format": "dd/MM/yyyy", "annualize": True},
}

try:
    for serie, config in SERIES.items():
        df = spark.read.parquet(f"file:///app/data/bronze/{serie}")

        silver_df = (
            df
            .withColumn("data",  to_date(col("data"), config["date_format"]))
            .withColumn("valor", col("valor").cast(DoubleType()))
        )

        if config["annualize"]:
            silver_df = silver_df.withColumn(
                "valor",
                spark_round(
                    ((pow(1 + col("valor") / 100, 252) - 1) * 100).cast(DoubleType()),
                    4
                )
            )

        validate_dataframe(silver_df, f"Silver {serie}")

        silver_df.coalesce(1).write             .format("delta")             .mode("overwrite")             .option("overwriteSchema", "true")             .save(f"file:///app/data/silver/{serie}")

        logger.info(f"Silver {serie} criada com sucesso")

    logger.info("Camada Silver completa")

except Exception as e:
    logger.error(f"Erro na Silver Layer: {e}")
    sys.exit(1)

finally:
    spark.stop()
