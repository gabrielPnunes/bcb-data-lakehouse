from pyspark.sql.functions import col, to_date
from processing.utils.spark_session import create_spark_session


spark = create_spark_session("SilverLayer")

df = spark.read.parquet("data/bronze/selic")

df_silver = (
    df
    .withColumn(
        "data",
        to_date(col("data"), "dd/MM/yyyy")
    )
    .withColumn(
        "valor",
        col("valor").cast("double")
    )
)

(
    df_silver.write
    .mode("overwrite")
    .parquet("data/silver/selic")
)

print("Camada/medalion Silver Criada")