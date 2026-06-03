import psycopg2
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "bcb_data",
    "user": "admin",
    "password": "admin",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_selic_anual():
    query = """
        SELECT ano, media_selic, classificacao_selic
        FROM analytics.mart_selic_anual
        ORDER BY ano
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def get_selic_raw():
    query = """
        SELECT ano, media_selic
        FROM public.gold_selic_anual
        ORDER BY ano
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)