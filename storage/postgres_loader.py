import pandas as pd
from sqlalchemy import create_engine

df = pd.read_parquet("data/gold/selic")

engine = create_engine(
    "postgresql://admin:admin@localhost:5432/bcb_data"
)

df.to_sql(
    "selic_gold",
    engine,
    if_exists="replace",
    index=False
)

print("Dados enviados ao PostgreSQL")