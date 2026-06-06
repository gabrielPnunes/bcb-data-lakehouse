from processing.spark_session import spark
from utils.logger import logger
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import sys

KAFKA_HOST = "kafka-bcb:9092"
TOPIC = "selic-stream"
OUTPUT_PATH = "file:///app/data/streaming/selic"
CHECKPOINT_PATH = "file:///app/data/streaming/checkpoints/selic"

schema = StructType([
    StructField("indicador", StringType(), True),
    StructField("ano",       IntegerType(), True),
    StructField("valor",     DoubleType(),  True),
])

try:
    df_raw = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_HOST)
        .option("subscribe", TOPIC)
        .option("startingOffsets", "earliest")
        .load()
    )

    df_parsed = (
        df_raw
        .select(from_json(col("value").cast("string"), schema).alias("data"))
        .select("data.*")
    )

    query = (
        df_parsed.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", CHECKPOINT_PATH)
        .start(OUTPUT_PATH)
    )

    logger.info("Spark Streaming iniciado — aguardando mensagens...")
    query.awaitTermination(timeout=60)
    logger.info("Streaming finalizado")

except Exception as e:
    logger.error(f"Erro no consumer: {e}")
    sys.exit(1)

finally:
    spark.stop()