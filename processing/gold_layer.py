from pyspark.sql import SparkSession
from pyspark.sql.functions import year, avg

spark = SparkSession.builder.getOrCreate()

df = spark.read.parquet("data/silver/selic")

df = df.withColumn("ano", year("data"))

gold_df = (
    df.groupBy("ano")
      .agg(
          avg("valor").alias("media_selic")
      )
      .orderBy("ano")
)

gold_df.show()

gold_df.write.mode("overwrite").parquet(
    "data/gold/selic"
)

print("Camada Gold criada")