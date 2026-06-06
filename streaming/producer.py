from kafka import KafkaProducer
from utils.logger import logger
import psycopg2
import json
import time
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": 5432,
    "dbname": "bcb_data",
    "user": "admin",
    "password": "admin",
}

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost:29092")
TOPIC = "selic-stream"


def get_selic_data():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT ano, media_selic FROM public.gold_selic_anual ORDER BY ano")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def run():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_HOST,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    rows = get_selic_data()

    logger.info(f"Publicando {len(rows)} registros no tópico {TOPIC}")

    for ano, media_selic in rows:
        message = {
            "indicador": "SELIC",
            "ano": ano,
            "valor": float(media_selic),
        }

        producer.send(TOPIC, value=message)
        logger.info(f"Publicado: {message}")
        time.sleep(1)

    producer.flush()
    producer.close()
    logger.info("Producer finalizado")


if __name__ == "__main__":
    run()