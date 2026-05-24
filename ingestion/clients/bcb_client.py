from datetime import datetime
from datetime import timedelta

import requests
import pandas as pd


class BCB_Client:

    BASE_URL = (
        "https://api.bcb.gov.br/dados/"
        "serie/bcdata.sgs.11/dados"
    )

    HEADERS = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    def get_selic(self):

        end_date = datetime.today()
        start_date = (
            end_date - timedelta(days = 365 * 10)
        )

        start_date = start_date.strftime(
            "%d/%m/%Y"
        )
        end_date = end_date.strftime(
            "%d/%m/%Y"
        )

        url = (
            f"{self.BASE_URL}"
            f"?formato=json"
            f"&dataInicial={start_date}"
            f"&dataFinal={end_date}"
        )

        response = requests.get(
            url,
            headers=self.HEADERS,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        return pd.DataFrame(data)