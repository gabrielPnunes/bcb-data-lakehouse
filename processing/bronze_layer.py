from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("BCB Bronze Layer")
    .getOrCreate()
)

df = spark.read.csv(
    "data/raw/selic/selic.csv",
    header=True,
    inferSchema=True
)

df.write.mode("overwrite").parquet(
    "data/bronze/selic"
)

print("Camada/medalion Bronze Criada")