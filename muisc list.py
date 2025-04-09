# Databricks notebook source
# dbutils.fs.cp("dbfs:/FileStore/tables/play1.json", "dbfs:/tmp/music/events/play1.json")
#dbutils.fs.cp("dbfs:/FileStore/tables/play1.json", "dbfs:/tmp/music/events/play2.json")
dbutils.fs.cp("dbfs:/FileStore/tables/play2.json", "dbfs:/tmp/music/events/play4.json")
dbutils.fs.cp("dbfs:/FileStore/tables/play3.json", "dbfs:/tmp/music/events/play5.json")

# COMMAND ----------

display(dbutils.fs.ls("/tmp/music/events/"))

# COMMAND ----------

# Load static reference data
songs = spark.read.option("header", True).csv("/FileStore/tables/songs.csv")
users = spark.read.option("header", True).csv("/FileStore/tables/users.csv")

# Streaming source using Autoloader
df_stream = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .option("cloudFiles.schemaLocation", "/tmp/music/schema") \
    .load("/tmp/music/events")

# Enrich with metadata
from pyspark.sql.functions import col

df_joined = df_stream \
    .join(users, "user_id", "left") \
    .join(songs, "song_id", "left") \
    .withColumn("event_time", col("timestamp").cast("timestamp"))

# Snowflake connection options

sfOptions = {
    "sfURL": "your link",
    "sfDatabase": "MY_FIRST_DB",
    "sfSchema": "MY_SCHEMA",
    "sfWarehouse": "COMPUTE_WH",
    "sfRole": "ACCOUNTADMIN",  # Optional
    "sfUser": "name",
    "sfPassword": "password",
    "dbtable": "MUSIC_EVENTS"
}
# Write stream to Snowflake using foreachBatch
def write_to_snowflake(batch_df, batch_id):
    batch_df.write \
        .format("snowflake") \
        .options(**sfOptions) \
        .mode("append") \
        .save()

df_joined.writeStream \
    .foreachBatch(write_to_snowflake) \
    .option("checkpointLocation", "/tmp/music/checkpoints/snowflake") \
    .start()
