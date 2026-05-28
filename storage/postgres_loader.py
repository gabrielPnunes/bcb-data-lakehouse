from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Postgres Loader") \
    .config(
        "spark.jars.packages",
        "org.postgresql:postgresql:42.7.3"
    ) \
    .getOrCreate()

df = spark.read.parquet("data/gold/selic")

print("Visualizando dados da Gold Layer")
df.show(5)

df.write \
    .format("jdbc") \
    .option(
        "url",
        "jdbc:postgresql://postgres-bcb:5432/bcb_data"
    ) \
    .option("dbtable", "gold_selic") \
    .option("user", "admin") \
    .option("password", "admin") \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

print("Dados enviados para PostgreSQL com sucesso")