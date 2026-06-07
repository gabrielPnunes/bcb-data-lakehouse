from processing.spark_session import spark
from ingestion.clients.bcb_client import fetch_serie
from utils.logger import logger
import sys

SERIES = ["selic", "ipca", "cambio", "cdi"]

try:
    for serie in SERIES:
        df_pd = fetch_serie(serie)
        df = spark.createDataFrame(df_pd)

        df.write.mode("overwrite").parquet(
            f"file:///app/data/bronze/{serie}"
        )

        logger.info(f"Bronze {serie}: {df.count()} registros salvos")

    logger.info("Camada Bronze criada com sucesso")

except Exception as e:
    logger.error(f"Erro na Bronze Layer: {e}")
    sys.exit(1)

finally:
    spark.stop()
