from utils.logger import logger


def validate_dataframe(df, layer_name):

    row_count = df.count()

    if row_count == 0:
        raise ValueError(f"{layer_name} está vazio")

    logger.info(f"{layer_name} validado com {row_count} linhas")