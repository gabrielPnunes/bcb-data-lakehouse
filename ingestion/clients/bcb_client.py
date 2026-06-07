import requests
import pandas as pd
from utils.logger import logger

BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados"

SERIES = {
    "selic":  11,
    "ipca":   433,
    "cambio": 1,
    "cdi":    12,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


def fetch_serie(serie_name: str, data_inicio: str = "01/01/2020") -> pd.DataFrame:
    serie_id = SERIES[serie_name]
    url = BASE_URL.format(serie=serie_id)

    params = {
        "formato":     "json",
        "dataInicial": data_inicio,
    }

    response = requests.get(url, params=params, headers=HEADERS, timeout=30)
    response.raise_for_status()

    df = pd.DataFrame(response.json())
    df.columns = ["data", "valor"]
    df["indicador"] = serie_name
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    logger.info(f"Serie {serie_name} ({serie_id}): {len(df)} registros")
    return df
