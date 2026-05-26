from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("BCB Gold Layer")
    .getOrCreate()
)

df = spark.read.parquet("data/silver/selic")

df.createOrReplaceTempView("selic")

gold_df = spark.sql("""
SELECT
    ano,
    AVG(valor) AS media_selic
FROM selic
GROUP BY ano
ORDER BY ano
""")

gold_df.write.mode("overwrite").parquet(
    "data/gold/selic"
)

print("Camada/medalion Gold criada")