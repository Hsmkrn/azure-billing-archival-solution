from pyspark.sql.functions import col, explode, year, month, dayofmonth, from_unixtime, current_timestamp

# Load Cosmos records (older than 90 days)
df = spark.read.format("cosmos.oltp").options(readConfig).load()
df_old = df.filter((current_timestamp().cast("long") - col("_ts")) > 90 * 86400)

# Write successful payments
df_success = df_old.filter(col("status") == "SUCCESS")
df_success.write.partitionBy("year", "month", "day").parquet("abfss://billing-archive@<storage>.dfs.core.windows.net/success/")

# Write failed payments
df_failed = df_old.filter(col("status") == "FAILED")
df_failed.write.partitionBy("year", "month", "day").parquet("abfss://billing-archive@<storage>.dfs.core.windows.net/failed/")

# Write items
df_items = df_old.select("userId", explode("items").alias("item"))
df_items.write.partitionBy("year", "month", "day").parquet("abfss://billing-archive@<storage>.dfs.core.windows.net/items/")
