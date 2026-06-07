from processing.spark_session import spark
from utils.logger import logger
import psycopg2
import sys
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": 5432,
    "dbname": "bcb_data",
    "user": "admin",
    "password": "admin",
}

JDBC_URL = "jdbc:postgresql://postgres-bcb:5432/bcb_data"
JDBC_PROPS = {
    "user": "admin",
    "password": "admin",
    "driver": "org.postgresql.Driver",
}

TABLES = {
    "file:///app/data/gold/selic_anual":   "gold_selic_anual",
    "file:///app/data/gold/ipca_anual":    "gold_ipca_anual",
    "file:///app/data/gold/cambio_anual":  "gold_cambio_anual",
    "file:///app/data/gold/cdi_anual":     "gold_cdi_anual",
    "file:///app/data/gold/taxa_real_anual": "gold_taxa_real_anual",
}


def truncate_table(table_name: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"TRUNCATE TABLE {table_name} CASCADE;")
        cur.close()
        conn.close()
        logger.info(f"Tabela {table_name} truncada")
    except Exception:
        logger.info(f"Tabela {table_name} não existe ainda — será criada")


try:
    for path, table in TABLES.items():
        truncate_table(table)

        df = spark.read.format("delta").load(path)

        df.write \
            .format("jdbc") \
            .option("url", JDBC_URL) \
            .option("dbtable", table) \
            .option("user", "admin") \
            .option("password", "admin") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()

        logger.info(f"{table} carregada com sucesso")

    logger.info("Carga PostgreSQL completa")

except Exception as e:
    logger.error(f"Erro no Load PostgreSQL: {e}")
    sys.exit(1)

finally:
    spark.stop()