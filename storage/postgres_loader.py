from processing.spark_session import spark
from config.settings import GOLD, DB_CONFIG, JDBC_URL, JDBC_PROPS
from utils.logger import logger
import psycopg2
import sys

TABLES = {
    GOLD["selic_anual"]:     "gold_selic_anual",
    GOLD["ipca_anual"]:      "gold_ipca_anual",
    GOLD["ipca_12m"]:        "gold_ipca_12m",
    GOLD["cambio_anual"]:    "gold_cambio_anual",
    GOLD["cdi_anual"]:       "gold_cdi_anual",
    GOLD["taxa_real_anual"]: "gold_taxa_real_anual",
}


def truncate_table(table_name: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table_name};")
        cur.close()
        conn.close()
        logger.info(f"Tabela {table_name} limpa")
    except Exception as e:
        logger.info(f"Tabela {table_name} nao existe ainda — sera criada")


try:
    for path, table in TABLES.items():
        truncate_table(table)

        df = spark.read.format("delta").load(path)

        df.write \
            .format("jdbc") \
            .option("url", JDBC_URL) \
            .option("dbtable", table) \
            .option("user", JDBC_PROPS["user"]) \
            .option("password", JDBC_PROPS["password"]) \
            .option("driver", JDBC_PROPS["driver"]) \
            .mode("append") \
            .save()

        logger.info(f"{table} carregada com sucesso")

    logger.info("Carga PostgreSQL completa")

except Exception as e:
    logger.error(f"Erro no Load PostgreSQL: {e}")
    sys.exit(1)

finally:
    spark.stop()