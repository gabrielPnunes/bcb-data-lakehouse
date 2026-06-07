import psycopg2
import pandas as pd
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": 5432,
    "dbname": "bcb_data",
    "user": "admin",
    "password": "admin",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_indicadores():
    query = """
        SELECT
            ano,
            media_selic,
            media_ipca,
            media_cdi,
            media_cambio,
            max_cambio,
            min_cambio,
            taxa_real,
            classificacao_selic
        FROM analytics.mart_indicadores_anual
        ORDER BY ano
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def get_selic_anual():
    query = """
        SELECT ano, media_selic, classificacao_selic
        FROM analytics.mart_selic_anual
        ORDER BY ano
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def get_ultimo_cambio():
    query = """
        SELECT valor, data
        FROM public.gold_cambio_anual
        ORDER BY ano DESC
        LIMIT 1
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)


def get_ipca_acumulado():
    query = """
        SELECT
            ano,
            SUM(media_ipca) as ipca_acumulado
        FROM public.gold_ipca_anual
        WHERE ano >= EXTRACT(YEAR FROM CURRENT_DATE) - 1
        GROUP BY ano
        ORDER BY ano
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)