from pathlib import Path

from ingestion.clients.bcb_client import BCB_Client
from ingestion.storage.database import engine

from ingestion.utils.logging import logger


class SelicIngestionService:

    def __init__(self):

        self.client = BCB_Client()

    def run(self):

        try:

            logger.info("Iniciando ingestão SELIC")

            df = self.client.get_selic()

            output_path = Path(
                "data/raw/selic"
            )
            output_path.mkdir(
                parents=True,
                exist_ok=True
            )

            file_path = (
                output_path / "selic.csv"
            )
            df.to_csv(
                file_path,
                index=False
            )
            logger.info(f"Arquivo salvo em: {file_path}")

            df.to_sql(
                "raw_selic",
                engine,
                if_exists="replace",
                index=False
            )
            logger.info(f"Dados salvos no PostgreSQL")


        except Exception as error:
            logger.error(f"Erro na ingestão: {error}")
            raise


if __name__ == "__main__":

    service = SelicIngestionService()
    service.run()