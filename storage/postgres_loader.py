from processing.spark_session import spark
from utils.logger import logger
import sys

try:
    df = spark.read \
        .format("delta") \
        .load("file:///app/data/gold/selic_anual")

    df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres-bcb:5432/bcb_data") \
        .option("dbtable", "gold_selic_anual") \
        .option("user", "admin") \
        .option("password", "admin") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    logger.info("Gold carregada no PostgreSQL com sucesso")

except Exception as e:
    logger.error(f"Erro no Load PostgreSQL: {e}")
    sys.exit(1)

finally:
    spark.stop()