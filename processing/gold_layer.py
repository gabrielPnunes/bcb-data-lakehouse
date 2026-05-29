from processing.spark_session import spark

from pyspark.sql.functions import year
from pyspark.sql.functions import avg


silver_df = (
    spark.read
    .format("delta")
    .load("data/silver/selic")
)

gold_df = (
    silver_df
    .withColumn(
        "ano",
        year("data")
    )
    .groupBy("ano")
    .agg(
        avg("valor").alias("media_selic")
    )
)

gold_df = gold_df.coalesce(1)

gold_df.write \
    .format("delta") \
    .mode("overwrite") \
    .save("data/gold/selic_anual")

print("Gold Layer criada")