from processing.spark_session import spark
from utils.logger import logger
import sys
import psycopg2

DB_CONFIG = {
    "host": "postgres-bcb",
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

try:

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE gold_selic_anual;")
    cur.close()
    conn.close()
    logger.info("Tabela gold_selic_anual truncada")

    df = spark.read \
        .format("delta") \
        .load("file:///app/data/gold/selic_anual")

    df.write \
        .format("jdbc") \
        .option("url", JDBC_URL) \
        .option("dbtable", "gold_selic_anual") \
        .option("user", "admin") \
        .option("password", "admin") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

    logger.info("Gold carregada no PostgreSQL com sucesso")

except Exception as e:
    logger.error(f"Erro no Load PostgreSQL: {e}")
    sys.exit(1)

finally:
    spark.stop()