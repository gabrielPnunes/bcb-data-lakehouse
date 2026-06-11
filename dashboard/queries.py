import psycopg2
import pandas as pd
from config.settings import DB_CONFIG
from datetime import datetime


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_indicadores() -> pd.DataFrame:
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


def get_kpis_ano_atual() -> pd.DataFrame:
    ano_atual = datetime.now().year
    query = f"""
        SELECT
            s.ultimo_selic,
            s.media_selic,
            i.ipca_acumulado,
            i12.ipca_12m,
            c.ultimo_cambio,
            d.ultimo_cdi,
            t.taxa_real                                              as taxa_real_ano,
            ROUND(CAST(s.ultimo_selic - i12.ipca_12m AS numeric), 2) as taxa_real_12m
        FROM public.gold_selic_anual s
        JOIN public.gold_ipca_anual i      ON s.ano = i.ano
        JOIN public.gold_ipca_12m i12      ON i12.ano = {ano_atual}
        JOIN public.gold_cambio_anual c    ON s.ano = c.ano
        JOIN public.gold_cdi_anual d       ON s.ano = d.ano
        JOIN public.gold_taxa_real_anual t ON s.ano = t.ano
        WHERE s.ano = {ano_atual}
    """
    with get_connection() as conn:
        return pd.read_sql(query, conn)